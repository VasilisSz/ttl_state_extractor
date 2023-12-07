
import cv2
import os
import pandas as pd
from tkinter import filedialog
from tkinter import Tk

# Function to get folder path
def get_folder_path():
    root = Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    folder_selected = filedialog.askdirectory() # show an "Open" dialog box and return the path to the selected folder
    return folder_selected

def draw_roi(frame, roi):
    x, y, w, h = roi
    cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

def select_roi(frame):
    r = cv2.selectROI("Select LED Area", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    return r

def select_new_roi(frame, old_roi):
    r = cv2.selectROI("Select new LED Area or press enter to keep the pre-selection", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    if r == (0, 0, 0, 0):
        return old_roi
    return r

def find_led_rois(folder_path):
    videos = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi'))]
    roi = None
    data = []

    for video in videos:
        video_path = os.path.join(folder_path, video)
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()

        if not ret:
            print(f"Failed to read video: {video}")
            continue
        
        if roi is None: # First video of the loop
            roi = select_roi(frame)
            draw_roi(frame, roi)
        elif roi is not None:
            draw_roi(frame, roi)

        # cv2.imshow("Select new? LED Area", frame)
        roi = select_new_roi(frame, roi)
        print(roi)
        key = cv2.waitKey(0)

        if key == 13:  # Enter key
            pass

        data.append({'Video': video, 'ROI': roi})
        cap.release()
        cv2.destroyAllWindows()

    df = pd.DataFrame(data)
    df.to_excel(os.path.join(folder_path, 'video_rois.xlsx'), index=False)
    return df



if __name__ == "__main__":
    folder_path = get_folder_path()
    roi_df = find_led_rois(folder_path)
