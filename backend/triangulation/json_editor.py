import json
import numpy as np
import tkinter as tk
from tkinter import messagebox

def save_data():
    try:
        # Get main values
        L, W, v = float(entry_L.get()), float(entry_W.get()), float(entry_v.get())
        x1, y1, t1 = float(entry_x1.get()), float(entry_y1.get()), float(entry_t1.get())
        x2, y2, t2 = float(entry_x2.get()), float(entry_y2.get()), float(entry_t2.get())
        x3, y3, t3 = float(entry_x3.get()), float(entry_y3.get()), float(entry_t3.get())

        # Get uncertainties
        dL, dW, dv = float(entry_dL.get()), float(entry_dW.get()), float(entry_dv.get())
        dx1, dy1, dt1 = float(entry_dx1.get()), float(entry_dy1.get()), float(entry_dt1.get())
        dx2, dy2, dt2 = float(entry_dx2.get()), float(entry_dy2.get()), float(entry_dt2.get())
        dx3, dy3, dt3 = float(entry_dx3.get()), float(entry_dy3.get()), float(entry_dt3.get())

        # Check limits
        if v <= 0 or dL < 0 or dW < 0 or dv < 0:
            messagebox.showerror("Error", "Velocity must be positive, and uncertainties must be non-negative.")
            return

        if not (0 <= x1 <= L and 0 <= y1 <= W and 0 <= x2 <= L and 0 <= y2 <= W and 0 <= x3 <= L and 0 <= y3 <= W):
            messagebox.showerror("Error", "x values must be between 0 and L, y values must be between 0 and W")
            return

        # Store data in NumPy arrays
        data_array = np.array([
            [L, W, v],  # First row contains parameters
            [x1, y1, t1], 
            [x2, y2, t2], 
            [x3, y3, t3]
        ])

        uncertainties_array = np.array([
            [dL, dW, dv],  # First row contains uncertainties for parameters
            [dx1, dy1, dt1], 
            [dx2, dy2, dt2], 
            [dx3, dy3, dt3]
        ])

        # Save to JSON
        with open('data.json', 'w') as f:
            json.dump(data_array.tolist(), f, indent=4)

        with open('uncertainties.json', 'w') as f:
            json.dump(uncertainties_array.tolist(), f, indent=4)

        messagebox.showinfo("Success", "Data and uncertainties saved successfully.")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Create Tkinter window
root = tk.Tk()
root.title("Data & Uncertainty Input")

# Create input fields
entry_L, entry_W, entry_v = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x1, entry_y1, entry_t1 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x2, entry_y2, entry_t2 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x3, entry_y3, entry_t3 = tk.Entry(root), tk.Entry(root), tk.Entry(root)

# Create uncertainty fields
entry_dL, entry_dW, entry_dv = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_dx1, entry_dy1, entry_dt1 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_dx2, entry_dy2, entry_dt2 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_dx3, entry_dy3, entry_dt3 = tk.Entry(root), tk.Entry(root), tk.Entry(root)

# Layout
labels = ["L", "W", "v", "x1", "y1", "t1", "x2", "y2", "t2", "x3", "y3", "t3"]
entries = [entry_L, entry_W, entry_v, entry_x1, entry_y1, entry_t1, entry_x2, entry_y2, entry_t2, entry_x3, entry_y3, entry_t3]

uncertainty_labels = ["ΔL", "ΔW", "Δv", "Δx1", "Δy1", "Δt1", "Δx2", "Δy2", "Δt2", "Δx3", "Δy3", "Δt3"]
uncertainty_entries = [entry_dL, entry_dW, entry_dv, entry_dx1, entry_dy1, entry_dt1, entry_dx2, entry_dy2, entry_dt2, entry_dx3, entry_dy3, entry_dt3]

# Create UI Grid
for i, (label, entry, u_label, u_entry) in enumerate(zip(labels, entries, uncertainty_labels, uncertainty_entries)):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
    entry.grid(row=i, column=1, padx=5, pady=2)

    tk.Label(root, text=u_label).grid(row=i, column=2, sticky="w", padx=5, pady=2)
    u_entry.grid(row=i, column=3, padx=5, pady=2)

# Save button
save_button = tk.Button(root, text="Save Data & Uncertainties", command=save_data)
save_button.grid(row=len(labels), column=0, columnspan=4, pady=10)

# Run the application
root.mainloop()
