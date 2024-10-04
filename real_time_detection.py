import cv2
import time  
from ultralytics import YOLO
from database import insert_brand_count, log_removal, fetch_removal_logs
from flask_socketio import SocketIO
from app import socketio  # Import socketio from the main app


# Load the YOLO model
model = YOLO('runs/detect/train6/weights/best.pt')  # Update the path to your best weights

# Define class names (update according to your dataset)
class_names = ["flake", "gold", "player"]  # Update class names if necessary

def process_webcam():
    # Open the webcam (0 for default camera, or change the index for external webcams)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow to avoid MSMF issues

    # Check if the webcam opened successfully
    if not cap.isOpened():
        print("Error opening webcam.")
        return None
    
    print("Emitting camera on status")
    socketio.emit('camera_status', {'status': 'on'})
    # Initialize counts for each brand (object class)
    brand_counts = {name: 0 for name in class_names}  # Dictionary to store counts
    previous_counts = brand_counts.copy()  # Initialize previous counts

    # Define time interval (in seconds) for database updates
    UPDATE_INTERVAL = 2  # Update the database every 2 seconds

    # Track the start time for updates
    start_time = time.time()

    # Process the webcam frames in real-time
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Perform YOLO detection on the current frame
        results = model(frame, conf=0.80)  # Adjust the confidence threshold if necessary

        # Reset current counts for each class (object)
        current_counts = {name: 0 for name in class_names}

        # Process results and draw bounding boxes on the frame
        for result in results:
            boxes = result.boxes  # Extract bounding boxes
            for box in boxes:
                if box.conf >= 0.80:  # Apply the confidence threshold
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Get bounding box coordinates
                    class_id = int(box.cls)  # Get the class index
                    
                    # Ensure the class_id is within the range of the class_names list
                    if class_id < len(class_names):
                        class_name = class_names[class_id]  # Get the class name
                        
                        # Count the number of boxes for each class (object)
                        current_counts[class_name] += 1
                        
                        # Draw the bounding box and class name on the frame
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f'{class_name}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


        # Check if the time interval for updating the database has passed
        current_time = time.time()
        if current_time - start_time >= UPDATE_INTERVAL:
            # Update the database if counts have changed
            for brand in class_names:
                if current_counts[brand] != previous_counts[brand]:
                    insert_brand_count(brand, current_counts[brand])  # Update the database
                    if current_counts[brand] < previous_counts[brand]:
                        removed_count = previous_counts[brand] - current_counts[brand]
                        log_removal(brand, previous_counts[brand], removed_count, current_counts[brand])  # Log removal

            
            
            # send_db_update()  # Call this function after the updates
            previous_counts = current_counts.copy()
            start_time = current_time


        # Display the processed frame in a window
        cv2.imshow('Webcam Feed', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    print("Emitting camera off status")
    socketio.emit('camera_status', {'status': 'off'})

    print("Webcam processing complete.")

# Call the function to start processing the webcam feed
process_webcam()