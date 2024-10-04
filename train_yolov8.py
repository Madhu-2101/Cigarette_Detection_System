
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Train the model
model.train(data='data.yaml', epochs=50, batch=16, imgsz=640, save=True)  # Adjust epochs and batch size as needed
