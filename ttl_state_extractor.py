import cv2
import os
import pandas as pd
import numpy as np
import pickle

def is_led_on(roi, threshold=245):
    # Check if the maximum brightness in the ROI is near 255
    return np.max(roi) >= threshold

def export_frame(video_name, frame_number, frame, state, images_path):
    # Create a filename based on video name, frame number, and state
    filename = f"{images_path}/{os.path.splitext(video_name)[0]}_frame{frame_number}_{state}.png"
    cv2.imwrite(filename, frame)

def get_led_states(roi_df, folder_path, images_path):
    led_states = {}
    
    for index, row in roi_df.iterrows():
        video_path = os.path.join(folder_path, row['Video'])
        print(video_path)
        roi = tuple(map(int, row['ROI'].strip('()').split(',')))
        cap = cv2.VideoCapture(video_path)

        frame_number = 0
        prev_frame = None
        prev_state = 0
        states = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            x, y, w, h = roi
            roi_frame = frame[y:y+h, x:x+w]
            state = is_led_on(roi_frame)

            # Export frames when LED is on or when the state changes
            if state or (state != prev_state):
                export_frame(row['Video'], frame_number, frame, 'ON' if state else 'OFF', images_path)
                if prev_frame is not None:
                    export_frame(row['Video'], frame_number-1, prev_frame, 'ON' if prev_state else 'OFF', images_path)

            prev_frame = frame.copy()
            prev_state = state
            states.append(int(state))
            frame_number += 1

        cap.release()
        led_states[row['Video']] = np.array(states)

    return led_states

if __name__ == '__main__':

    roi_df_path = ''    
    folder_path = 'videos'
    images_path = 'images'

    roi_df = pd.read_excel(roi_df_path)

    led_states = get_led_states(roi_df, folder_path, images_path)
    
    with open('led_states.pickle', "wb") as f:
        pickle.dump(led_states, f, pickle.HIGHEST_PROTOCOL)

