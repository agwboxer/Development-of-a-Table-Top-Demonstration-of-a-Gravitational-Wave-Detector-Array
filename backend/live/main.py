import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # Fix OpenMP conflict

import cv2
import argparse
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import time

plt.switch_backend('TkAgg')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='YOLOv8 Live Ball Tracking')
    parser.add_argument(
        '--webcam-resolution',
        default=[640, 480],
        nargs=2,
        type=int
    )
    parser.add_argument(
        '--camera-index',
        default=0,
        type=int,
        help='Index of the camera to use (0, 1, etc.)'
    )
    args = parser.parse_args()
    return args

class DisplacementPlot:
    def __init__(self, max_points=50):
        self.max_points = max_points
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')
        self.displacement_data = deque(maxlen=max_points)
        self.time_data = deque(maxlen=max_points)
        self.start_time = time.time()

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Displacement (pixels)')
        self.ax.set_title('Ball Displacement Over Time')
        plt.show(block=False) 

    def update_plot(self, frame):
        if len(self.time_data) > 0:
            self.line.set_data(self.time_data, self.displacement_data)
            self.ax.relim()
            self.ax.autoscale_view()
        return self.line,

    def add_point(self, displacement):
        current_time = time.time() - self.start_time
        self.time_data.append(current_time)
        self.displacement_data.append(displacement)
        
        if current_time > self.ax.get_xlim()[1]:
            self.ax.set_xlim(0, current_time + 1)
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

def calculate_displacement(prev_point, current_point):
    if prev_point is None or current_point is None:
        return 0
    return np.sqrt((current_point[0] - prev_point[0]) ** 2 + (current_point[1] - prev_point[1]) ** 2)

def main():
    args = parse_args()
    frame_width, frame_height = args.webcam_resolution
    camera_index = args.camera_index

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera at index {camera_index}")
        print("Available cameras:")
        for i in range(3):  
            test_cap = cv2.VideoCapture(i)
            if test_cap.isOpened():
                print(f"Camera found at index {i}")
                test_cap.release()
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    try:
        model = YOLO('yolov8n.pt')  
    except Exception as e:
        print(f"Error loading model: {e}")
        cap.release()
        return

    trajectory = []
    plot = DisplacementPlot()
    prev_point = None

    ani = FuncAnimation(
        plot.fig,
        plot.update_plot,
        interval=50,
        cache_frame_data=False,
        blit=True
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame from camera")
            break

        try:
            results = model(frame)
        except Exception as e:
            print(f"Error during detection: {e}")
            continue

        current_point = None

        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                if 'ball' in label.lower():
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    current_point = (cx, cy)
                    trajectory.append(current_point)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if current_point is not None:
            displacement = calculate_displacement(prev_point, current_point)
            plot.add_point(displacement)
            prev_point = current_point

        for i in range(1, len(trajectory)):
            if trajectory[i - 1] is None or trajectory[i] is None:
                continue
            cv2.line(frame, trajectory[i - 1], trajectory[i], (255, 0, 0), 2)

        cv2.imshow('Ball Tracking', frame)

        if cv2.getWindowProperty('Ball Tracking', cv2.WND_PROP_VISIBLE) < 1:
            break
        if not plt.fignum_exists(plot.fig.number):
            break

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.close(plot.fig)

if __name__ == '__main__':
    main()
