import json
import numpy as np
import tkinter as tk
from tkinter import messagebox

def save_data():
    try:
        L = float(entry_L.get())
        W = float(entry_W.get())
        v = float(entry_v.get())

        if v <= 0:
            messagebox.showerror("Error", "Velocity (v) must be positive")
            return

        # Get values from entry fields
        x1, y1, t1 = float(entry_x1.get()), float(entry_y1.get()), float(entry_t1.get())
        x2, y2, t2 = float(entry_x2.get()), float(entry_y2.get()), float(entry_t2.get())
        x3, y3, t3 = float(entry_x3.get()), float(entry_y3.get()), float(entry_t3.get())

        # Check limits
        if not (0 <= x1 <= L and 0 <= y1 <= W and 0 <= x2 <= L and 0 <= y2 <= W and 0 <= x3 <= L and 0 <= y3 <= W):
            messagebox.showerror("Error", "x values must be between 0 and L, y values must be between 0 and W")
            return

        # Store data in a NumPy array
        data_array = np.array([
            [L, W, v],  # First row contains parameters
            [x1, y1, t1], 
            [x2, y2, t2], 
            [x3, y3, t3]
        ])

        # Convert NumPy array to list before saving to JSON
        with open('data.json', 'w') as f:
            json.dump(data_array.tolist(), f, indent=4)

        messagebox.showinfo("Success", "Data saved to data.json")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Create Tkinter window
root = tk.Tk()
root.title("JSON Data Input")

# Create input fields
entry_L, entry_W, entry_v = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x1, entry_y1, entry_t1 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x2, entry_y2, entry_t2 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x3, entry_y3, entry_t3 = tk.Entry(root), tk.Entry(root), tk.Entry(root)

# Layout
labels = ["L", "W", "v", "x1", "y1", "t1", "x2", "y2", "t2", "x3", "y3", "t3"]
entries = [entry_L, entry_W, entry_v, entry_x1, entry_y1, entry_t1, entry_x2, entry_y2, entry_t2, entry_x3, entry_y3, entry_t3]
for i, (label, entry) in enumerate(zip(labels, entries)):
    tk.Label(root, text=label).grid(row=i // 3, column=(i % 3) * 2)
    entry.grid(row=i // 3, column=(i % 3) * 2 + 1)

# Save button
save_button = tk.Button(root, text="Save to JSON", command=save_data)
save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
