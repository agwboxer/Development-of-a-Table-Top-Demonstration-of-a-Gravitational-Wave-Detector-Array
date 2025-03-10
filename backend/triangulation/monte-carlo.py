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

num_samples = 1000  
source_positions = np.zeros((num_samples, 2))  

for i in range(num_samples):
    t1_sample = np.random.normal(t1, dt1)
    t2_sample = np.random.normal(t2, dt2)
    t3_sample = np.random.normal(t3, dt3)
    v_sample = np.random.normal(v, dv)

    x1_sample = np.random.normal(x1, dx1)
    y1_sample = np.random.normal(y1, dy1)
    x2_sample = np.random.normal(x2, dx2)
    y2_sample = np.random.normal(y2, dy2)
    x3_sample = np.random.normal(x3, dx3)
    y3_sample = np.random.normal(y3, dy3)

    delta_t12_sample = t2_sample - t1_sample
    delta_t13_sample = t3_sample - t1_sample
    delta_d12_sample = v_sample * delta_t12_sample
    delta_d13_sample = v_sample * delta_t13_sample

    detector_positions_sample = np.array([
        [x1_sample, y1_sample],
        [x2_sample, y2_sample],
        [x3_sample, y3_sample]
    ])

    result = minimize(distance_difference, initial_guess,
                      args=(detector_positions_sample, delta_d12_sample, delta_d13_sample))

    source_positions[i] = result.x

mean_source_position = np.mean(source_positions, axis=0)
std_source_position = np.std(source_positions, axis=0)

print(f"Mean source position: ({mean_source_position[0]:.2f}, {mean_source_position[1]:.2f})")
print(f"Uncertainty in source position (x, y): ({std_source_position[0]:.2f}, {std_source_position[1]:.2f})")

plt.figure(figsize=(10, 8))
plt.scatter(source_positions[:, 0], source_positions[:, 1], alpha=0.5, label='Monte Carlo Samples')
plt.errorbar(mean_source_position[0], mean_source_position[1], xerr=std_source_position[0], yerr=std_source_position[1],
             fmt='o', color='red', label='Mean Source Position', capsize=5)
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.xlim(0,L)
plt.ylim(0,W)
plt.show()
