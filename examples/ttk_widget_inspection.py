import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

from serializer import BSerialized
root = tk.Tk()
root.title("Introspection Test Window")
root.geometry("800x500")
root.configure(bg="#222222")  # ttk widgets ignore this, but tk widgets still use it

# ---------------------------------------------------------
# BUTTON (default ttk)
# ---------------------------------------------------------
btn = ttk.Button(root, text="Click Me")
btn.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.12)

# ---------------------------------------------------------
# LABEL (default ttk)
# ---------------------------------------------------------
lbl = ttk.Label(
    root,
    text="A multi-line label\nwith wraplength and justify",
    anchor="nw",
    justify="left",
)
lbl.place(relx=0.35, rely=0.05, relwidth=0.25, relheight=0.2)

# ---------------------------------------------------------
# ENTRY (default ttk)
# ---------------------------------------------------------
entry = ttk.Entry(root)
entry.insert(0, "Type here…")
entry.place(relx=0.65, rely=0.05, relwidth=0.3, relheight=0.1)

# ---------------------------------------------------------
# CHECKBUTTON (default ttk)
# ---------------------------------------------------------
chk_var = tk.BooleanVar(value=True)
chk = ttk.Checkbutton(
    root,
    text="Enable Feature",
    variable=chk_var,
)
chk.place(relx=0.05, rely=0.25, relwidth=0.25, relheight=0.08)

# ---------------------------------------------------------
# RADIOBUTTONS (default ttk)
# ---------------------------------------------------------
radio_var = tk.StringVar(value="A")

r1 = ttk.Radiobutton(
    root,
    text="Option A",
    variable=radio_var,
    value="A",
)
r1.place(relx=0.05, rely=0.35, relwidth=0.25, relheight=0.07)

r2 = ttk.Radiobutton(
    root,
    text="Option B",
    variable=radio_var,
    value="B",
)
r2.place(relx=0.05, rely=0.43, relwidth=0.25, relheight=0.07)

# ---------------------------------------------------------
# FRAME WITH CHILDREN (default ttk)
# ---------------------------------------------------------
frame = ttk.Frame(root)
frame.place(relx=0.35, rely=0.3, relwidth=0.3, relheight=0.3)

frame_lbl = ttk.Label(
    frame,
    text="Inside Frame",
    anchor="center",
)
frame_lbl.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.25)

frame_btn = ttk.Button(
    frame,
    text="Inner Button",
)
frame_btn.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.35)

# ---------------------------------------------------------
# TEXT WIDGET (tk only)
# ---------------------------------------------------------
txt = tk.Text(
    root,
    font=("Courier New", 11),
    fg="#DDDDDD",
    bg="#111111",
    insertbackground="white",
    wrap="word",
    relief="ridge",
    bd=4,
)
txt.insert("1.0", "This is a Text widget.\nIt has multiple lines.\nUseful for introspection.")
txt.place(relx=0.67, rely=0.2, relwidth=0.28, relheight=0.4)

# ---------------------------------------------------------
# COMBOBOX (default ttk)
# ---------------------------------------------------------
combo = ttk.Combobox(
    root,
    values=["Alpha", "Beta", "Gamma", "Delta"],
    state="readonly",
)
combo.current(1)
combo.place(relx=0.05, rely=0.55, relwidth=0.25, relheight=0.08)

# ---------------------------------------------------------
# SCALE (default ttk)
# ---------------------------------------------------------
scale = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
)
scale.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

# ---------------------------------------------------------
# LISTBOX (tk only)
# ---------------------------------------------------------
listbox = tk.Listbox(
    root,
    font=("Arial", 12),
    fg="white",
    bg="#000000",
    selectbackground="#4444AA",
    activestyle="dotbox",
)
for item in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert("end", item)
listbox.place(relx=0.67, rely=0.65, relwidth=0.28, relheight=0.25)


for item in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert("end", item)
listbox.place(relx=0.67, rely=0.65, relwidth=0.28, relheight=0.25)

new_serializer = BSerialized()

new_configuration = new_serializer(root)

new_serializer.save_configuration("examples/tkinter_window_test.json", new_configuration)
