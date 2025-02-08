import json
import numpy as np
import tkinter as tk
from tkinter import messagebox

def save_data():
    try:
        # Get values from entry fields
        x1, y1, t1 = float(entry_x1.get()), float(entry_y1.get()), float(entry_t1.get())
        x2, y2, t2 = float(entry_x2.get()), float(entry_y2.get()), float(entry_t2.get())
        x3, y3, t3 = float(entry_x3.get()), float(entry_y3.get()), float(entry_t3.get())
        
        # Store data in a NumPy array
        data = np.array([[x1, y1, t1], [x2, y2, t2], [x3, y3, t3]])
        
        # Save as JSON
        with open('data.json', 'w') as f:
            json.dump(data.tolist(), f)
        
        messagebox.showinfo("Success", "Data saved to data.json")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers")

# Create Tkinter window
root = tk.Tk()
root.title("JSON Data Input")

# Create input fields
entry_x1, entry_y1, entry_t1 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x2, entry_y2, entry_t2 = tk.Entry(root), tk.Entry(root), tk.Entry(root)
entry_x3, entry_y3, entry_t3 = tk.Entry(root), tk.Entry(root), tk.Entry(root)

# Layout
labels = ["x1", "y1", "t1", "x2", "y2", "t2", "x3", "y3", "t3"]
entries = [entry_x1, entry_y1, entry_t1, entry_x2, entry_y2, entry_t2, entry_x3, entry_y3, entry_t3]
for i, (label, entry) in enumerate(zip(labels, entries)):
    tk.Label(root, text=label).grid(row=i // 3, column=(i % 3) * 2)
    entry.grid(row=i // 3, column=(i % 3) * 2 + 1)

# Save button
save_button = tk.Button(root, text="Save to JSON", command=save_data)
save_button.grid(row=4, column=0, columnspan=6)

# Run the application
root.mainloop()