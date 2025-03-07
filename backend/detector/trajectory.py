import json
import matplotlib.pyplot as plt
import numpy as np


def plot_distance(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    if not data or len(data) < 2:
        print("Not enough data points to calculate distances.")
        return

    distances = []
    distance_errors = []
    times = []  # List to store time in seconds

    frame_rate = 30  # 30 frames per second

    for i in range(1, len(data)):
        dx = data[i]["cx"] - data[i - 1]["cx"]
        dy = data[i]["cy"] - data[i - 1]["cy"]
        distance = np.sqrt(dx ** 2 + dy ** 2)

        uncertainty_dx = 1
        uncertainty_dy = 1
        distance_error = np.sqrt((dx / distance * uncertainty_dx) ** 2 + (dy / distance * uncertainty_dy) ** 2)

        distances.append(distance)
        distance_errors.append(distance_error)

        # Calculate time in seconds
        time = i / frame_rate
        times.append(time)

    plt.figure(figsize=(8, 6))
    plt.errorbar(times, distances, yerr=distance_errors, marker='o', linestyle='-', color='b',
                 label='Distance between Points')

    plt.xlabel("Time (seconds)")
    plt.ylabel("Distance travelled between frames (pix)")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    json_file = "output.json"
    plot_distance(json_file)
