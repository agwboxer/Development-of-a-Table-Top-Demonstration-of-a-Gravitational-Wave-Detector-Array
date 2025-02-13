import numpy as np
import matplotlib.pyplot as plt
import json

# Load the JSON files
with open('data.json', 'r') as f:
    data = json.load(f)

with open('uncertainties.json', 'r') as f:
    uncertainties = json.load(f) 

# Extract data and uncertainties
dC, d1, d2, d3 = uncertainties
constants, C1, C2, C3 = data

x1, y1, t1 = C1
x2, y2, t2 = C2
x3, y3, t3 = C3
L, W, v = constants

dL, dW, dv = dC
dx1, dy1, dt1 = d1
dx2, dy2, dt2 = d2
dx3, dy3, dt3 = d3

# Calculate delta_d and their uncertainties
delta_d_12 = v * (t2 - t1)
d_delta_d_12 = np.sqrt( (dv*(t2 - t1))**2 + (v*dt2)**2 + (v*dt1)**2 )

delta_d_13 = v * (t3 - t1)
d_delta_d_13 = np.sqrt( (dv*(t3 - t1))**2 + (v*dt3)**2 + (v*dt1)**2 )

delta_d_23 = v * (t3 - t2)
d_delta_d_23 = np.sqrt( (dv*(t3 - t2))**2 + (v*dt3)**2 + (v*dt2)**2 )

# Create grid
x = np.linspace(0, L, 4000)
y = np.linspace(0, W, 4000)
X, Y = np.meshgrid(x, y)

# Compute distances and their uncertainties
epsilon = 1e-9  # Avoid division by zero

D1 = np.sqrt((x2 - X)**2 + (y2 - Y)**2)
D2 = np.sqrt((x1 - X)**2 + (y1 - Y)**2)
D3 = np.sqrt((x3 - X)**2 + (y3 - Y)**2)

# Uncertainties in distances
dD1 = np.sqrt( (( (x2 - X)/(D1 + epsilon) * dx2 ))**2 + (( (y2 - Y)/(D1 + epsilon) * dy2 ))**2 )
dD2 = np.sqrt( (( (x1 - X)/(D2 + epsilon) * dx1 ))**2 + (( (y1 - Y)/(D2 + epsilon) * dy1 ))**2 )
dD3 = np.sqrt( (( (x3 - X)/(D3 + epsilon) * dx3 ))**2 + (( (y3 - Y)/(D3 + epsilon) * dy3 ))**2 )

# Compute Z values and their uncertainties
Z12 = D1 - D2 - delta_d_12
dZ12 = np.sqrt(dD1**2 + dD2**2 + d_delta_d_12**2)

Z13 = D1 - D3 - delta_d_13
dZ13 = np.sqrt(dD1**2 + dD3**2 + d_delta_d_13**2)

Z23 = D2 - D3 - delta_d_23
dZ23 = np.sqrt(dD2**2 + dD3**2 + d_delta_d_23**2)

# Create masks for uncertainty regions (1-sigma)
mask12 = np.abs(Z12) <= dZ12
mask13 = np.abs(Z13) <= dZ13
mask23 = np.abs(Z23) <= dZ23

# Plot settings
plt.figure(figsize=(10, 8))

# Plot uncertainty regions
plt.contourf(X, Y, mask12, levels=[0.5, 1.5], colors='blue', alpha=0.2, label="Uncertainty (Hyperbola 12)")
plt.contourf(X, Y, mask13, levels=[0.5, 1.5], colors='green', alpha=0.2, label="Uncertainty (Hyperbola 13)")
plt.contourf(X, Y, mask23, levels=[0.5, 1.5], colors='red', alpha=0.2, label="Uncertainty (Hyperbola 23)")

# Plot hyperbolas
plt.contour(X, Y, Z12, levels=[0], colors='blue', linewidths=2, label="Hyperbola 12")
plt.contour(X, Y, Z13, levels=[0], colors='green', linewidths=2, label="Hyperbola 13")
plt.contour(X, Y, Z23, levels=[0], colors='red', linewidths=2, label="Hyperbola 23")

# Plot detectors with error bars
plt.errorbar([x1, x2, x3], [y1, y2, y3], 
             xerr=[dx1, dx2, dx3], 
             yerr=[dy1, dy2, dy3], 
             fmt='o', color='black', label="Detectors",
             ecolor='black', elinewidth=1, capsize=4, linestyle='None')

# Axes and labels
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, L)
plt.ylim(0, W)
plt.gca().set_aspect('equal')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend(loc='upper right', fontsize=10)

plt.show()
