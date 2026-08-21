import cv2
import os

vidcap = cv2.VideoCapture('C:/Users/Biomed/Documents/bmi_Aus/scratch_video.mp4')
for s in [12.6, 12.7, 12.8, 12.9, 13.1, 13.2]:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, s * 1000)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(f'C:/Users/Biomed/Documents/bmi_Aus/frame_{s}.jpg', image)
        print(f"Saved frame_{s}.jpg")
    else:
        print(f"Failed to read frame at {s} seconds")
