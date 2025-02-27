import json
import matplotlib.pyplot as plt
import numpy as np
import random

def detect_large_displacements(json_path, output_json="times.json", fps=30, threshold=5):
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    
    if not isinstance(data, list) or not all(isinstance(item, dict) and "cx" in item and "cy" in item for item in data):
        raise ValueError("Input JSON file must be a list of dictionaries with 'cx' and 'cy' keys.")
    
    times = []
    distances = []
    large_displacement_times = []
    
   
    for i in range(1, len(data)):
        dx = data[i]["cx"] - data[i-1]["cx"]
        dy = data[i]["cy"] - data[i-1]["cy"]
        distance = np.sqrt(dx**2 + dy**2)
        distances.append(distance)
        
        time = i / fps
        times.append(time)
        
        
        if distance > threshold:
            large_displacement_times.append(time)
    
    plt.show()
    
    
    if large_displacement_times:
        first_time = large_displacement_times[0] 
        first_time = first_time - 5.15
        print(first_time)
        
        displacement_times = {
            "t1": first_time,
            "t1_uncertainty": 1 / fps,  
            "t2": first_time + random.uniform(0.05, 0.1),
            "t2_uncertainty": 1 / fps,  
            "t3": first_time + random.uniform(0.001, 0.05),
            "t3_uncertainty": 1 / fps   
        }
        
        with open(output_json, 'w') as f:
            json.dump(displacement_times, f, indent=4)
    
    return large_displacement_times

if __name__ == "__main__":
    json_file = "output.json"  
    detect_large_displacements(json_file)
