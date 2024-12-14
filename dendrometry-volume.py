import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from tkinter import filedialog,messagebox
from tkinter import ttk
# Calculate cone volume
def coneVolume(diameter, height):
    return (1/12) * np.pi * (diameter ** 2) * height

# Calculate cylinder volume
def cylinderVolume(diameter, height):
    return (1/4) * np.pi * (diameter ** 2) * height

# Get diameter
def get_diameter(file):
    df = pd.read_csv(file).to_numpy()
    points = df[:, :2]
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    north = np.max(hull_points[:, 1])
    south = np.min(hull_points[:, 1])
    east = np.max(hull_points[:, 0])
    west = np.min(hull_points[:, 0])
    crown_width1 = (north - south) / 2
    crown_width2 = (east - west) / 2
    crown_diameter = round((crown_width1 + crown_width2) / 2,3)
    return crown_diameter

# get crown height
def get_crown_height(file):
    df = pd.read_csv(file).to_numpy()
    points = df[:, :3]
    z_max = np.max(points[:, 2])
    z_min = np.min(points[:, 2])
    crown_height = round(z_max - z_min, 3)
    return crown_height

# Dealing with the process of calculating volume
def on_process_clone():
    files = filedialog.askopenfilenames(
        initialdir=".",
        title="select CSV files",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    results = []
    for file_path in files:
        crown_diameter = get_diameter(file_path)
        crown_height = get_crown_height(file_path)
        volume = round(coneVolume(crown_diameter, crown_height), 3)
        results.append(f"filename: {file_path}, diameter: {crown_diameter:.3f}, crown_height: {crown_height:.3f}, clone-volume: {volume:.3f}")
        tree.insert("", "end", values=(file_path, crown_diameter, crown_height, volume))
    display_results(results)

# Dealing with the process of calculating volume
def on_process_cylinder():
    files = filedialog.askopenfilenames(
        initialdir=".",
        title="select CSV files",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    results = []
    for file_path in files:
        crown_diameter = get_diameter(file_path)
        crown_height = get_crown_height(file_path)
        volume = round(cylinderVolume(crown_diameter, crown_height),3)
        results.append(f"filename: {file_path}, diameter: {crown_diameter:.3f}, crown_height: {crown_height:.3f}, cylinder-volume: {volume:.3f}")
        tree.insert("", "end", values=(file_path, crown_diameter, crown_height, volume))
    display_results(results)


# Display results
def display_results(results):
    result_text.config(state=tk.NORMAL)
    #result_text.delete(1.0, tk.END)
    for result in results:
        result_text.insert(tk.END, result + "\n")
    result_text.config(state=tk.DISABLED)

#Copying table to clipboard
def on_treeview_heading_click(event):
    #Copy the contents of a Treeview to the clipboard when a column heading is clicked.
    region = tree.identify("region", event.x, event.y)
    if region == "heading": 
        col = tree.identify_column(event.x)  
        col_index = int(col.replace("#", "")) - 1  # adjust for zero-based index
        # 提取整列数据
        column_data = []
        for row_id in tree.get_children():  # iterate through rows
            row_values = tree.item(row_id, "values")  # get all values of row
            if len(row_values) > col_index:  # check if column index exists 
                column_data.append(row_values[col_index])
        #transform to string
        data = "\n".join(column_data)
        root.clipboard_clear()
        root.clipboard_append(data)
        messagebox.showinfo("Copied", "Copied to clipboard")

# GUI layout
root = tk.Tk()
root.title("Volume Calculator")
root.geometry("800x500")
root.resizable(width=True, height=True)
root.config(bg="lightblue")

label_title = tk.Label(root, text="Volume Calculator", font=("Arial", 20), bg="lightblue")
label_title.pack(padx=10, pady=10)

process_button_clone = tk.Button(root, text="select files by clone volume", command=on_process_clone)
process_button_clone.pack(padx=10, pady=10)

process_button_cylinder = tk.Button(root, text="select files by cylinder volume", command=on_process_cylinder)
process_button_cylinder.pack(padx=10, pady=10)

# Add result text
result_text = tk.Text(root, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED, bg="white")
result_text.pack(padx=10, pady=10)
 
#Add tree view
tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', height=5)
tree.pack(fill=tk.BOTH, expand=True)
tree.column("#1")
tree.heading("#1", text="filename")
tree.column("#2" )
tree.heading("#2", text="radius")
tree.column("#3")
tree.heading("#3", text="crown_height")
tree.column("#4")
tree.heading("#4", text="volume")
# click to copy
tree.bind('<ButtonRelease-1>', on_treeview_heading_click)
root.mainloop()
