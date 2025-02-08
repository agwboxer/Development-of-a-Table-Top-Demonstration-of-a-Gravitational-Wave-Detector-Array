import cv2
import os


def save_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0

    while True:
        # Read the next frame from the video
        ret, frame = cap.read()

        # If the frame was not grabbed, we've reached the end of the video
        if not ret:
            break

        # Save the frame as an image file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    # Release the video capture object
    cap.release()
    print(f"Finished extracting {frame_count} frames.")



video_path = r"C:\Users\agwbo\Desktop\dissertation\test-data-1-23_1\test1.mp4"

output_folder = r"C:\Users\agwbo\Desktop\dissertation\frames"

save_frames(video_path, output_folder)
