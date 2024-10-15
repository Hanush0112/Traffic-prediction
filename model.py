import cv2
import numpy as np
from ultralytics import YOLO
from collections import defaultdict

# Load YOLO Model
model = YOLO('yolov8n.pt')
video = 'sample3.mp4'
# Open the video file or specify the webcam (0) if needed
cap = cv2.VideoCapture(video)  # Change '0' to your IP camera URL if needed
fps = cap.get(cv2.CAP_PROP_FPS)

# Define line position and variables
line_position_incoming = 250  # Position for the incoming lane line (right lane)
line_thickness = 2

crossed_vehicles = defaultdict(float)  # Store time at which vehicle crossed the line
waiting_time_threshold = 120  # Waiting time threshold in seconds
waiting_times = defaultdict(float)  # Track the waiting time for each vehicle
is_congested = False  # Flag for congestion
overall_traffic_status = []  # Store traffic status

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame with the YOLO model
    results = model(frame)[0]

    # Draw the line for the incoming lane (right lane)
    cv2.line(frame, (0, line_position_incoming), (frame.shape[1], line_position_incoming), (0, 255, 0), line_thickness)  # Incoming lane (Green)

    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Current time in seconds

    for detection in results.boxes:
        x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy().astype(int)
        class_id = int(detection.cls.item())

        if class_id in [2, 3, 5, 7]:  # car, truck, bus, motorbike
            vehicle_bottom_y = y2
            vehicle_x_center = (x1 + x2) // 2
            vehicle_id = detection.id.item() if detection.id is not None else f"{x1}-{y1}"

            # Check if the vehicle is in the right lane and below the line
            if vehicle_bottom_y >= line_position_incoming and vehicle_x_center >= frame.shape[1] // 2:
                if vehicle_id not in crossed_vehicles:
                    crossed_vehicles[vehicle_id] = current_time  # Start counting waiting time
                    waiting_times[vehicle_id] = 0  # Initialize waiting time
                    print(f"Vehicle {vehicle_id} crossed the line (right lane) at {current_time:.2f} seconds.")

            # Update waiting time for vehicles still waiting
            if vehicle_id in crossed_vehicles:
                waiting_times[vehicle_id] = current_time - crossed_vehicles[vehicle_id]  # Update waiting time

            # Check if the vehicle has waited longer than the threshold
            if waiting_times[vehicle_id] >= waiting_time_threshold:
                is_congested = True
                if "Incoming Traffic Detected" not in overall_traffic_status:
                    overall_traffic_status.append("Incoming Traffic Detected")
                cv2.putText(frame, "Traffic Detected (Incoming)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Display waiting time on the frame
            cv2.putText(frame, f"Wait Time: {waiting_times[vehicle_id]:.1f}s", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # Reset congestion flag if no vehicles are waiting
    if is_congested and not any(waiting_time >= waiting_time_threshold for waiting_time in waiting_times.values()):
        print("This road is clear.")
        is_congested = False
        overall_traffic_status.append("Road Clear")

    # Display clear status on the frame
    if not is_congested:
        cv2.putText(frame, "Road is Clear", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Display the frame
    cv2.imshow('Traffic Congestion Detection for Right Lane', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# Output traffic detection status
if is_congested:
    a = 1 # Traffic detected
else:
    a = 0  # No traffic detected
