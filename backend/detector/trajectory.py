import json
import matplotlib.pyplot as plt
import numpy as np

def plot_distance(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if not data or len(data) < 2:
        print("Not enough data points to calculate distances.")
        return
    
    distances = []
    distance_errors = []
    
    for i in range(1, len(data)):
        dx = data[i]["cx"] - data[i-1]["cx"]
        dy = data[i]["cy"] - data[i-1]["cy"]
        distance = np.sqrt(dx**2 + dy**2)
        
        uncertainty_dx = 1
        uncertainty_dy = 1
        distance_error = np.sqrt((dx / distance * uncertainty_dx)**2 + (dy / distance * uncertainty_dy)**2)
        
        distances.append(distance)
        distance_errors.append(distance_error)
    
    plt.figure(figsize=(8, 6))
    plt.errorbar(range(1, len(distances) + 1), distances, yerr=distance_errors, marker='o', linestyle='-', color='b', label='Distance between Points')
    
    plt.xlabel("Index Number")
    plt.ylabel("Distance between Points")
    plt.title("Distance between Consecutive Bob Positions")
    plt.legend()
    
    plt.show()

if __name__ == "__main__":
    json_file = "output.json"
    plot_distance(json_file)
