# README.md for LED ROI and State Extraction Scripts

This README provides instructions on how to use two Python scripts: `define_LED_rois.py` and `ttl_state_extractor.py`. These scripts are part of a workflow for identifying regions of interest (ROIs) in video frames where LEDs are present and then extracting the on/off states of these LEDs from the videos.

## Prerequisites

Before running these scripts, ensure you have the following:
1. Python installed on your system.
2. Required Python libraries: `cv2`, `os`, `pandas`, `numpy`, `tkinter`, `pickle`.

## Script 1: define_LED_rois.py

### Purpose
This script is used to define and select regions of interest (ROIs) in video frames where LEDs are located. It allows users to manually select these areas in each video.

### Steps to Run
1. Run `define_LED_rois.py`.
2. A file dialog will open. Select the folder containing your video files.
3. The script will load each video in the selected folder.
4. For each video, a window will pop up allowing you to select the ROI where the LED is located. Use your mouse to draw a rectangle around this area.
5. Press `Enter` to confirm the selection. If you need to reselect the ROI, the script will allow you to do so.
6. The script will save the ROI data for each video in an Excel file named `video_rois.xlsx` in the same folder.

## Script 2: ttl_state_extractor.py

### Purpose
After defining the ROIs, this script analyzes the video frames to determine the on/off state of the LEDs based on brightness within the selected ROIs.

### Steps to Run
1. Before running `ttl_state_extractor.py`, ensure that the `video_rois.xlsx` file generated by the first script is in the same folder as your videos.
2. Edit `ttl_state_extractor.py`:
   - Set `roi_df_path` to the path of your `video_rois.xlsx` file.
   - Set `folder_path` to the path of your videos.
   - Set `images_path` to the path where you want to save the extracted frames.
3. Run `ttl_state_extractor.py`.
4. The script will process each video and determine the LED states (on or off) for each frame. It will also save frames where the LED state changes to the specified `images_path`.
5. LED state data is saved in a pickle file named `led_states.pickle`.

## Note
- Ensure that the videos are in a supported format (`.mp4`, `.avi`).
- The scripts require manual intervention for selecting ROIs. Be consistent with ROI selection across videos for accurate results.