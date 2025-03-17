
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import json

with open('data.json', 'r') as f:
    data = json.load(f)

with open('uncertainties.json', 'r') as f:
    uncertainties = json.load(f)

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
    with open('ToAs.json', 'r') as f:
        times_data = json.load(f)
    t1 = times_data["t1"]
    dt1 = times_data["combined_dt1"]
    t2 = times_data["t2"]
    dt2 = times_data["combined_dt2"]
    t3 = times_data["t3"]
    dt3 = times_data["combined_dt3"]
else:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

dC, d1, d2, d3 = uncertainties
constants, C1, C2, C3 = data

x1, y1, _ = C1
x2, y2, _ = C2
x3, y3, _ = C3
L, W, v = constants

dL, dW, dv = dC
dx1, dy1, _ = d1
dx2, dy2, _ = d2
dx3, dy3, _ = d3

detector_positions = np.array([
    [x1, y1],
    [x2, y2],
    [x3, y3]
])

delta_t12 = t2 - t1
delta_t13 = t3 - t1
delta_t23 = t3 - t2

delta_d12 = v * delta_t12
delta_d13 = v * delta_t13
delta_d23 = v * delta_t23


def distance_difference(position, detector_positions, delta_d12, delta_d13):
    x, y = position
    d1 = np.sqrt((x - detector_positions[0, 0]) ** 2 + (y - detector_positions[0, 1]) ** 2)
    d2 = np.sqrt((x - detector_positions[1, 0]) ** 2 + (y - detector_positions[1, 1]) ** 2)
    d3 = np.sqrt((x - detector_positions[2, 0]) ** 2 + (y - detector_positions[2, 1]) ** 2)

    diff1 = d2 - d1 - delta_d12
    diff2 = d3 - d1 - delta_d13

    return diff1 ** 2 + diff2 ** 2


initial_guess = np.mean(detector_positions, axis=0)

result = minimize(distance_difference, initial_guess, args=(detector_positions, delta_d12, delta_d13))
estimated_position = result.x
print(f"Estimated position: ({estimated_position[0]:.2f}, {estimated_position[1]:.2f})")


x = np.linspace(0, L, 500)
y = np.linspace(0, W, 500)
X, Y = np.meshgrid(x, y)

Z = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = distance_difference([X[i, j], Y[i, j]], detector_positions, delta_d12, delta_d13)

plt.figure(figsize=(10, 8))
contour = plt.contour(X, Y, Z, levels=20, cmap='viridis')
plt.colorbar(contour, label='Distance Difference Function')
plt.scatter(mean_source_position[0], mean_source_position[1], color='red', label='Mean Source Position')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Source Function (Distance Difference)')
plt.legend()
plt.xlim(0, L)
plt.ylim(0, W)
plt.show()
