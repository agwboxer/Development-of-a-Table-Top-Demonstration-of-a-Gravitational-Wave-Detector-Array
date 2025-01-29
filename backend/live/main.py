import cv2
import argparse
import numpy as np
from ultralytics import YOLO

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='YOLOv8 Live Ball Tracking')
    parser.add_argument(
        '--webcam-resolution', 
        default=[640, 480], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    frame_width, frame_height = args.webcam_resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    model = YOLO('yolov8l.pt')
    trajectory = []  # List to store ball positions

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame)
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                if 'ball' in label.lower():  # Check if detected object is a ball
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Compute center of ball
                    trajectory.append((cx, cy))  # Store ball position
                    
                    # Draw bounding box and center
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw trajectory
        for i in range(1, len(trajectory)):
            if trajectory[i - 1] is None or trajectory[i] is None:
                continue
            cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 0, 0), 2)
        
        cv2.imshow('Ball Tracking', frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
