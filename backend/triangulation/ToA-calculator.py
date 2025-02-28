import numpy as np
import matplotlib.pyplot as plt
import json

with open('data.json', 'r') as f:
    data = json.load(f)

with open('uncertainties.json', 'r') as f:
    uncertainties = json.load(f)

constants = data[0]  
L, W, v = constants
dL, dW, dv = uncertainties[0]  
x1, y1, _ = data[1] 
x2, y2, _ = data[2]  
x3, y3, _ = data[3]  

try:
    source_x = float(input("Enter the X coordinate of the source: "))
    source_y = float(input("Enter the Y coordinate of the source: "))
except ValueError:
    print("Invalid input. Please enter valid numbers for X and Y.")
    exit()

D1 = np.sqrt((x1 - source_x)**2 + (y1 - source_y)**2)
D2 = np.sqrt((x2 - source_x)**2 + (y2 - source_y)**2)
D3 = np.sqrt((x3 - source_x)**2 + (y3 - source_y)**2)

dD1 = np.sqrt(((x1 - source_x) / D1 * dL)**2 + ((y1 - source_y) / D1 * dW)**2)
dD2 = np.sqrt(((x2 - source_x) / D2 * dL)**2 + ((y2 - source_y) / D2 * dW)**2)
dD3 = np.sqrt(((x3 - source_x) / D3 * dL)**2 + ((y3 - source_y) / D3 * dW)**2)

t1 = D1 / v 
t2 = D2 / v 
t3 = D3 / v 

dt1 = np.sqrt((dD1 / v)**2 + (dL / v)**2)
dt2 = np.sqrt((dD2 / v)**2 + (dL / v)**2)
dt3 = np.sqrt((dD3 / v)**2 + (dL / v)**2)

result = {
    "X": source_x,
    "Y": source_y,
    "D1": D1,
    "D2": D2,
    "D3": D3,
    "dD1": dD1,
    "dD2": dD2,
    "dD3": dD3,
    "t1": t1,
    "t2": t2,
    "t3": t3,
    "dt1": dt1,
    "dt2": dt2,
    "dt3": dt3
}

with open('times_reversed.json', 'w') as f:
    json.dump(result, f, indent=4)

X_grid = np.linspace(0, L, 400)
Y_grid = np.linspace(0, W, 400)
X, Y = np.meshgrid(X_grid, Y_grid)

plt.figure(figsize=(10, 6))
plt.contour(X, Y, (X - x1)**2 + (Y - y1)**2, levels=[D1**2], colors='red')
plt.contour(X, Y, (X - x2)**2 + (Y - y2)**2, levels=[D2**2], colors='green')
plt.contour(X, Y, (X - x3)**2 + (Y - y3)**2, levels=[D3**2], colors='blue')
plt.scatter([x1, x2, x3], [y1, y2, y3], color='black', label='Detectors')
plt.scatter(source_x, source_y, color='purple', label='Source')
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
