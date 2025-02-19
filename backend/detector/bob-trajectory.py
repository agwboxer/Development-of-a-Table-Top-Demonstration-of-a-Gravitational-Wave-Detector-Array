import json
import matplotlib.pyplot as plt
import numpy as np

def plot_distance(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if not data or len(data) < 2:
        print("Not enough data points to calculate distances.")
        return
    
    distances = [
        np.sqrt((data[i]["cx"] - data[i-1]["cx"])**2 + (data[i]["cy"] - data[i-1]["cy"])**2)
        for i in range(1, len(data))
    ]
    
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(distances) + 1), distances, marker='o', linestyle='-', color='b', label='Distance between Points')
    
    plt.xlabel("Index Number")
    plt.ylabel("Distance between Points")
    plt.title("Distance between Consecutive Bob Positions")
    plt.legend()
    plt.grid(True)
    
    plt.show()

if __name__ == "__main__":
    json_file = "output.json"  # Change this to the correct path if needed
    plot_distance(json_file)