import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import json

# Load the JSON files
with open('data.json', 'r') as f:
    data = json.load(f)

with open('uncertainties.json', 'r') as f:
    uncertainties = json.load(f)

# Prompt the user to choose which file to use for times
choice = input("Choose the source of times (1 for times.json, 2 for times_reversed.json): ").strip()

if choice == '1':
    with open('times.json', 'r') as f:
        times_data = json.load(f)
    t1 = times_data["t1"]
    dt1 = times_data["t1_uncertainty"]
    t2 = times_data["t2"]
    dt2 = times_data["t2_uncertainty"]
    t3 = times_data["t3"]
    dt3 = times_data["t3_uncertainty"]
elif choice == '2':
    with open('times_reversed.json', 'r') as f:
        times_data = json.load(f)
    t1 = times_data["t1"]
    dt1 = times_data["dt1"]
    t2 = times_data["t2"]
    dt2 = times_data["dt2"]
    t3 = times_data["t3"]
    dt3 = times_data["dt3"]
else:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

# Extract data and uncertainties
dC, d1, d2, d3 = uncertainties
constants, C1, C2, C3 = data

x1, y1, _ = C1
x2, y2, _ = C2 
x3, y3, _ = C3  
L, W, v = constants  # Length, Width, wave speed

dL, dW, dv = dC
dx1, dy1, _ = d1 
dx2, dy2, _ = d2 
dx3, dy3, _ = d3 

# Detector positions
detector_positions = np.array([
    [x1, y1],  # Detector 1
    [x2, y2],  # Detector 2
    [x3, y3]   # Detector 3
])

# Time differences
delta_t12 = t2 - t1  # t2 - t1
delta_t13 = t3 - t1  # t3 - t1
delta_t23 = t3 - t2  # t3 - t2

# Distance differences
delta_d12 = v * delta_t12
delta_d13 = v * delta_t13
delta_d23 = v * delta_t23

# Function to minimize
def distance_difference(position, detector_positions, delta_d12, delta_d13):
    x, y = position
    d1 = np.sqrt((x - detector_positions[0, 0])**2 + (y - detector_positions[0, 1])**2)
    d2 = np.sqrt((x - detector_positions[1, 0])**2 + (y - detector_positions[1, 1])**2)
    d3 = np.sqrt((x - detector_positions[2, 0])**2 + (y - detector_positions[2, 1])**2)
    
    diff1 = d2 - d1 - delta_d12
    diff2 = d3 - d1 - delta_d13
    
    return diff1**2 + diff2**2

# Initial guess (midpoint of detectors)
initial_guess = np.mean(detector_positions, axis=0)

# Minimize the function
result = minimize(distance_difference, initial_guess, args=(detector_positions, delta_d12, delta_d13))

# Estimated position
estimated_position = result.x
print(f"Estimated position: ({estimated_position[0]:.2f}, {estimated_position[1]:.2f})")

# Function to plot hyperbola with uncertainty
def plot_hyperbola_with_uncertainty(detector1, detector2, delta_d, ax, color, label, source_position):
    x1, y1 = detector1
    x2, y2 = detector2
    
    # Generate points for the hyperbola
    x = np.linspace(0, L, 500)
    y = np.linspace(0, W, 500)
    X, Y = np.meshgrid(x, y)
    
    # Hyperbola equation: |d2 - d1| = delta_d
    d1 = np.sqrt((X - x1)**2 + (Y - y1)**2)
    d2 = np.sqrt((X - x2)**2 + (Y - y2)**2)
    hyperbola = np.abs(d2 - d1) - np.abs(delta_d)
    
    # Filter out the branch that does not contain the source
    # Use the source position to determine the correct branch
    source_d1 = np.sqrt((source_position[0] - x1)**2 + (source_position[1] - y1)**2)
    source_d2 = np.sqrt((source_position[0] - x2)**2 + (source_position[1] - y2)**2)
    if source_d2 - source_d1 < 0:
        hyperbola = -hyperbola  # Flip the hyperbola branch
    
    # Plot the hyperbola
    ax.contour(X, Y, hyperbola, levels=[0], colors=color, label=label)
    
    # Propagate uncertainty in the hyperbola
    # Uncertainty in delta_d due to uncertainties in time differences and wave speed
    delta_d_uncertainty = np.sqrt((v * dt1)**2 + (v * dt2)**2 + (delta_t12 * dv)**2)
    
    # Plot uncertainty as a shaded region around the hyperbola
    ax.contourf(X, Y, np.abs(hyperbola), levels=[0, delta_d_uncertainty], colors=color, alpha=0.2)

# Create plot
plt.figure(figsize=(10, 8))
ax = plt.gca()

# Plot detectors with error bars
plt.errorbar(x1, y1, xerr=dx1, yerr=dy1, fmt='o', color='red', label='Detector 1', capsize=5)
plt.errorbar(x2, y2, xerr=dx2, yerr=dy2, fmt='o', color='green', label='Detector 2', capsize=5)
plt.errorbar(x3, y3, xerr=dx3, yerr=dy3, fmt='o', color='purple', label='Detector 3', capsize=5)

# Plot estimated source position with error bars
source_x_uncertainty = np.sqrt(dx1**2 + dx2**2 + dx3**2) / 3
source_y_uncertainty = np.sqrt(dy1**2 + dy2**2 + dy3**2) / 3
plt.errorbar(estimated_position[0], estimated_position[1], xerr=source_x_uncertainty, yerr=source_y_uncertainty, fmt='o', color='blue', label='Source', capsize=5)

# Plot hyperbolas with uncertainty
plot_hyperbola_with_uncertainty(detector_positions[0], detector_positions[1], delta_d12, ax, 'green', 'Hyperbola (D1-D2)', estimated_position)
plot_hyperbola_with_uncertainty(detector_positions[0], detector_positions[2], delta_d13, ax, 'purple', 'Hyperbola (D1-D3)', estimated_position)
plot_hyperbola_with_uncertainty(detector_positions[1], detector_positions[2], delta_d23, ax, 'orange', 'Hyperbola (D2-D3)', estimated_position)

# Plot settings
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.xlim(0, L)
plt.ylim(0, W)

# Show plot
plt.show()
