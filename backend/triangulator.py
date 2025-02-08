import numpy as np
import matplotlib.pyplot as plt
import json

# Load the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)  # This will be a list of lists

# Extract rows into separate lists
constants, C1, C2, C3 = data

x1, y1, t1 = C1
x2, y2, t2 = C2
x3, y3, t3 = C3
L, W, v = constants

# Calculate the distances from time differences
delta_d_12 = v * (t2 - t1)
delta_d_13 = v * (t3 - t1)
delta_d_23 = v * (t3 - t2)

# Create a grid of (x, y) points
x = np.linspace(0, L, 400)
y = np.linspace(0, W, 400)
X, Y = np.meshgrid(x, y)

# Compute hyperbolic functions
D1 = np.sqrt((x2 - X)**2 - (y2 - Y)**2)
D2 = np.sqrt((x1 - X)**2 - (y1 - Y)**2)
D3 = np.sqrt((x3 - X)**2 - (y3 - Y)**2)

# Compute level sets where the equations hold
Z12 = D1 - D2
Z13 = D1 - D3 
Z23 = D2 - D3 

# Plot the contours where Z = 0 (hyperbolas)
plt.figure(figsize=(8, 6))
plt.contour(X, Y, Z12, levels=[0], colors='b', linewidths=2, label="Hyperbola 12")
plt.contour(X, Y, Z13, levels=[0], colors='g', linewidths=2, label="Hyperbola 13")
plt.contour(X, Y, Z23, levels=[0], colors='r', linewidths=2, label="Hyperbola 23")

# Mark the reference points
plt.scatter([x1, x2, x3], [y1, y2, y3], color='black', marker='o', label="Reference Points")

# Axes settings
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xlim(0, L)
plt.ylim(0, W)
plt.gca().set_aspect('equal')
plt.legend()
plt.title("Hyperbolic Locus from Time Differences")

# Show plot
plt.show()
