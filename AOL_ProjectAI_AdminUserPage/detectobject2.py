import cv2
from ultralytics import YOLO
import json
import sys

#model = YOLO("combined_dataset/runs/detect/train/weights/best.pt")
model = YOLO("yolov8n.pt")
#print("Model labels:", model.names, file=sys.stderr)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    print(json.dumps([]))
    exit()

frame = cv2.resize(frame, (640, 640))
cv2.imwrite("debug_frame.jpg", frame)  

results = model(frame, imgsz=640, verbose=False)

detected = set()
if results and results[0].boxes is not None:
    for box in results[0].boxes:
        class_id = int(box.cls.item())
        label = model.names[class_id]
        detected.add(label)

print(json.dumps(list(detected)))