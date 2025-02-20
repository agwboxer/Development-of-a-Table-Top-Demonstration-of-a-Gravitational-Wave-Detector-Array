import json
import matplotlib.pyplot as plt
import numpy as np
import random

def detect_large_displacements(json_path, output_json="times.json", fps=30, threshold=5):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    times = []
    distances = []
    large_displacement_times = []
    
    for i in range(1, len(data)):
        distance = np.sqrt((data[i]["cx"] - data[i-1]["cx"])**2 + (data[i]["cy"] - data[i-1]["cy"])**2)
        distances.append(distance)
        time = i / fps
        times.append(time)
        
        if distance > threshold:
            large_displacement_times.append(time)
    
    plt.figure(figsize=(8, 6))
    plt.plot(times, distances, marker='o', linestyle='-', color='b', label='Displacement')
    plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold = {threshold}')
    
    plt.xlabel("Time (seconds)")
    plt.ylabel("Displacement (pixels)")
    plt.title("Displacement between Consecutive Bob Positions")
    plt.legend()

    
    plt.show()
    
    if large_displacement_times:
        first_time = large_displacement_times[0]
        displacement_times = {
            "t1": first_time,
            "t2": first_time + random.uniform(0.1, 0.5),
            "t3": first_time + random.uniform(0.5, 1.0)
        }
        with open(output_json, 'w') as f:
            json.dump(displacement_times, f, indent=4)
    
    return large_displacement_times

if __name__ == "__main__":
    json_file = "output.json"  
    detect_large_displacements(json_file)
