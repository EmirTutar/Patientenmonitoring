import torch
import numpy as np
import random
import cv2

# Load model
model = torch.hub.load("ultralytics/yolov5", "custom", path="model.pt", device='cpu', trust_repo=True)

# Open videostream
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# Specify image size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Loop through videoframes
while cap.isOpened():
    # Read frame
    success, frame = cap.read()
    # Convert to rgb color
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if success:
        # Do inference
        results = model(rgb_image)
        
        # Print inference result
        results.print()
    else:
        # Break after Videostream closes
        break

# Free videostream
cap.release()
