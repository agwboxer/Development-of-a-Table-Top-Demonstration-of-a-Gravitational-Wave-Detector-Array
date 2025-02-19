import cv2
import argparse
import numpy as np
from ultralytics import YOLO
import os
import json  

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='YOLOv8 Ball Tracking on Images')
    parser.add_argument('--image_folder', type=str, required=True, help='Path to the folder containing images')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to save processed images')
    parser.add_argument('--output_json', type=str, default='output.json', help='Path to save the JSON file with central positions')
    return parser.parse_args()

def main():
    args = parse_args()
    image_folder = args.image_folder
    output_folder = args.output_folder
    output_json = args.output_json  

    os.makedirs(output_folder, exist_ok=True)  # Create output folder if not exists

    model = YOLO('trained.pt')
    trajectory = []  
    central_positions = []  

    image_files = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg'))])

    for image_file in image_files:
        frame = cv2.imread(image_file)
        if frame is None:
            print(f"Failed to load image: {image_file}")
            continue

        results = model(frame)
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                if 'bob' in label.lower():  
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  
                    trajectory.append((cx, cy))  
                    central_positions.append({"image": os.path.basename(image_file), "cx": cx, "cy": cy})  
                    
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, "Bob", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        for i in range(1, len(trajectory)):
            if trajectory[i - 1] is None or trajectory[i] is None:
                continue
            cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 0, 0), 2)

        output_path = os.path.join(output_folder, os.path.basename(image_file))
        cv2.imwrite(output_path, frame)  # Save processed frame
    
    with open(output_json, 'w') as f:
        json.dump(central_positions, f, indent=4)
    print(f"Processed images saved to {output_folder}")
    print(f"Central positions saved to {output_json}")

if __name__ == '__main__':
    main()
