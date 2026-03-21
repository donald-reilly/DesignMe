import tkinter as tk
from tkinter import ttk

from figman import FigMan
from serializer import BSerialized
from constructor import BConstructed

root = tk.Tk()
root.title("TTK Widget Demo (No Frames)")
root.geometry("900x550")
root.configure(bg="#2b2b2b")

# ------------------------------------------------
# STYLE SETUP
# ------------------------------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Demo.TButton",
    font=("Segoe UI", 10),
    padding=6
)

style.configure(
    "Demo.TLabel",
    font=("Segoe UI", 10)
)

# ------------------------------------------------
# TITLE LABEL
# ------------------------------------------------

title = ttk.Label(
    root,
    text="TTK Styled Demo Window",
    style="Demo.TLabel",
    font=("Segoe UI", 14, "bold")
)

title.place(relx=0.03, rely=0.03)

# ------------------------------------------------
# BUTTON
# ------------------------------------------------

btn = ttk.Button(
    root,
    text="Click Me",
    style="Demo.TButton"
)

btn.place(relx=0.03, rely=0.12, relwidth=0.18)

# ------------------------------------------------
# ENTRY
# ------------------------------------------------

entry = ttk.Entry(root)
entry.insert(0, "Type something here...")
entry.place(relx=0.25, rely=0.12, relwidth=0.25)

# ------------------------------------------------
# COMBOBOX
# ------------------------------------------------

combo = ttk.Combobox(
    root,
    values=["Option A", "Option B", "Option C"],
    state="readonly"
)

combo.current(0)
combo.place(relx=0.55, rely=0.12, relwidth=0.2)

# ------------------------------------------------
# CHECKBUTTON
# ------------------------------------------------

check_var = tk.BooleanVar()

check = ttk.Checkbutton(
    root,
    text="Enable Feature",
    variable=check_var
)

check.place(relx=0.03, rely=0.22)

# ------------------------------------------------
# RADIOBUTTONS
# ------------------------------------------------

radio_var = tk.StringVar(value="A")

radio_a = ttk.Radiobutton(
    root,
    text="Choice A",
    variable=radio_var,
    value="A"
)

radio_b = ttk.Radiobutton(
    root,
    text="Choice B",
    variable=radio_var,
    value="B"
)

radio_a.place(relx=0.03, rely=0.30)
radio_b.place(relx=0.03, rely=0.36)

# ------------------------------------------------
# PROGRESSBAR
# ------------------------------------------------

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate"
)

progress["value"] = 65
progress.place(relx=0.25, rely=0.30, relwidth=0.25)

# ------------------------------------------------
# SCALE
# ------------------------------------------------

scale = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal"
)

scale.place(relx=0.55, rely=0.30, relwidth=0.25)

# ------------------------------------------------
# TREEVIEW
# ------------------------------------------------

tree = ttk.Treeview(
    root,
    columns=("A", "B"),
    show="headings",
    height=5
)

tree.heading("A", text="Column A")
tree.heading("B", text="Column B")

tree.insert("", "end", values=("Row 1", "Value 1"))
tree.insert("", "end", values=("Row 2", "Value 2"))
tree.insert("", "end", values=("Row 3", "Value 3"))

tree.place(relx=0.03, rely=0.45, relwidth=0.45, relheight=0.3)

# ------------------------------------------------
# NOTEBOOK
# ------------------------------------------------

notebook = ttk.Notebook(root)
notebook.place(relx=0.52, rely=0.45, relwidth=0.45, relheight=0.3)

tab1 = ttk.Button(notebook, text="Tab 1 Content")
tab2 = ttk.Button(notebook, text="Tab 2 Content")

notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

ttk.Label(tab1, text="Content inside tab 1").pack(pady=20)
ttk.Label(tab2, text="Content inside tab 2").pack(pady=20)

# ------------------------------------------------
# TEXT (tk widget)
# ------------------------------------------------

text = tk.Text(
    root,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)

text.insert("1.0", "tk.Text widget\nUseful for editing large text.")
text.place(relx=0.03, rely=0.80, relwidth=0.45, relheight=0.15)

# ------------------------------------------------
# LISTBOX (tk widget)
# ------------------------------------------------

listbox = tk.Listbox(
    root,
    bg="#1e1e1e",
    fg="white",
    selectbackground="#4444aa"
)

for item in ["Alpha", "Beta", "Gamma", "Delta"]:
    listbox.insert("end", item)

listbox.place(relx=0.52, rely=0.80, relwidth=0.45, relheight=0.15)

new_serializer = BSerialized()
new_constructor = BConstructed()

new_configuration = new_serializer(root)

root.mainloop()
