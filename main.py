import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image

class DraggableListbox(tk.Listbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Double-1>', self.on_double_click)
        self.drag_data = {"start_index": None, "item": None}

    def on_click(self, event):
        self.drag_data["start_index"] = self.nearest(event.y)

    def on_drag(self, event):
        index = self.nearest(event.y)
        if index != self.drag_data["start_index"]:
            self.selection_clear(self.drag_data["start_index"])
            self.selection_set(index)

    def on_release(self, event):
        end_index = self.nearest(event.y)
        start_index = self.drag_data["start_index"]
        if start_index != end_index:
            item = self.get(start_index)
            self.delete(start_index)
            self.insert(end_index, item)
        self.selection_clear(0, tk.END)

    def on_double_click(self, event):
        try:
            index = self.nearest(event.y)
            self.delete(index)
        except IndexError:
            pass

def add_dura():
    user_input = simpledialog.askstring("Duration", "Enter the number of seconds for aligned frame:")
    if user_input:
        try:
            listbox_duras.insert(tk.END, str(float(user_input)))
        except:
            pass

def add_folder():
    directory = filedialog.askdirectory(title="Select a Folder")
    if directory:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                listbox_images.insert(tk.END, item_path)

def compile_list():
    images = []
    durations = []
    for i in range(listbox_images.size()):
        images.append(Image.open(listbox_images.get(i)))
    for i in range(listbox_duras.size()):
        durations.append(float(listbox_duras.get(i))*1000)
    if len(images) != len(durations):
        messagebox.showwarning("Length Mismatch", "Each frame must have a duration numerical")
    if len(images) == 0:
        return
    save_to = file_path = filedialog.asksaveasfilename(
        defaultextension=".gif",
        filetypes=[("Gif Animation", "*.gif"), ("All files", "*.*")],
        title="Save as"
    )
    if not save_to:
        return
    images[0].save(
        save_to,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0 if is_looped.get() else 1
    )

r = tk.Tk()
r.title("fta")
frame_main = tk.Frame(r)
frame_main.pack(pady=(10, 0))
frame_images = tk.Frame(frame_main)
frame_images.pack(pady=(10, 0))
listbox_images = DraggableListbox(frame_images, width=60, height=20)
listbox_images.pack(side=tk.LEFT, padx=(0, 10))
listbox_duras = DraggableListbox(frame_images, width=60, height=20)
listbox_duras.pack(side=tk.LEFT)
frame_controls = tk.Frame(frame_main)
frame_controls.pack(pady=10, padx=10)
images_add_button = tk.Button(frame_controls, text="Add Directory", command=add_folder)
images_add_button.pack(side=tk.LEFT, padx=5)
dura_add_button = tk.Button(frame_controls, text="Add Duration", command=add_dura)
dura_add_button.pack(side=tk.LEFT, padx=5)
compile_button = tk.Button(frame_controls, text="Compile", command=compile_list)
compile_button.pack(side=tk.LEFT, padx=5)
is_looped = tk.IntVar()
loop_enabled = tk.Checkbutton(frame_controls, text="Animation Loop?", variable=is_looped)
loop_enabled.pack(pady=10)
r.mainloop()
