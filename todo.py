import tkinter as tk
from tkinter import messagebox
import os

TASK_FILE = "tasks.txt"


def load_tasks():
    """Load saved tasks from file."""
    task_list.delete(0, tk.END)
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for task in file.readlines():
                task_list.insert(tk.END, task.strip())


def save_tasks():
    """Save tasks to file."""
    with open(TASK_FILE, "w") as file:
        tasks = task_list.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")


def add_task():
    task = entry.get().strip()
    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return
    task_list.insert(tk.END, f"[ ]  {task}")
    entry.delete(0, tk.END)
    save_tasks()


def delete_task():
    try:
        task_list.delete(task_list.curselection()[0])
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task to delete!")


def clear_all():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
        task_list.delete(0, tk.END)
        save_tasks()


def mark_completed(event=None):
    index = task_list.curselection()
    if not index:
        return

    idx = index[0]
    task = task_list.get(idx)

    if task.startswith("[ ]"):
        task_list.delete(idx)
        task_list.insert(idx, task.replace("[ ]", "[✔]"))
    else:
        task_list.delete(idx)
        task_list.insert(idx, task.replace("[✔]", "[ ]"))

    save_tasks()


def edit_task():
    index = task_list.curselection()
    if not index:
        messagebox.showwarning("Warning", "Select a task to edit!")
        return

    idx = index[0]
    task_text = task_list.get(idx)[4:]  # remove checkbox symbol
    entry.delete(0, tk.END)
    entry.insert(tk.END, task_text)

    def update():
        new_task = entry.get().strip()
        if new_task != "":
            task_list.delete(idx)
            task_list.insert(idx, f"[ ]  {new_task}")
            entry.delete(0, tk.END)
            save_tasks()
            edit_win.destroy()

    edit_win = tk.Toplevel(app)
    edit_win.title("Edit Task")
    edit_win.geometry("300x140")
    edit_win.configure(bg=bg_color)

    tk.Label(edit_win, text="Edit your task:", bg=bg_color, fg=fg_color, font=("Segoe UI", 12, "bold")).pack(pady=10)
    tk.Entry(edit_win, textvariable=tk.StringVar(value=task_text), font=("Segoe UI", 14), width=22).pack(pady=5)
    tk.Button(edit_win, text="Save", bg="#27AE60", fg="white", font=("Segoe UI", 11), command=update).pack(pady=8)


def filter_tasks(event=None):
    search_text = search.get().lower()
    task_list.delete(0, tk.END)

    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            for task in file.readlines():
                if search_text in task.lower():
                    task_list.insert(tk.END, task.strip())


def toggle_theme():
    global bg_color, fg_color, button_color

    if app["bg"] == "#101820":
        bg_color = "white"
        fg_color = "black"
        button_color = "#4B70F5"
    else:
        bg_color = "#101820"
        fg_color = "white"
        button_color = "#4CAF50"

    app.configure(bg=bg_color)
    title.configure(bg=bg_color, fg=fg_color)
    search_label.configure(bg=bg_color, fg=fg_color)

    entry.configure(bg="white")
    search_entry.configure(bg="white")

    for widget in button_frame.winfo_children():
        widget.configure(bg=button_color)

    task_list.configure(bg="#333333" if bg_color == "#101820" else "#e6e6e6", fg="white" if bg_color == "#101820" else "black")


# ---------------- GUI Window ----------------
app = tk.Tk()
app.title("✨ Beautiful Advanced To-Do List")
app.geometry("500x620")
app.configure(bg="#101820")

bg_color = "#101820"
fg_color = "white"
button_color = "#4CAF50"

# Title
title = tk.Label(app, text="✅ ADVANCED TO-DO LIST ✅",
                 font=("Segoe UI", 22, "bold"), bg=bg_color, fg=fg_color)
title.pack(pady=10)

# Search bar
search = tk.StringVar()
search_label = tk.Label(app, text="🔎 Search Tasks:", bg=bg_color, fg=fg_color, font=("Segoe UI", 11))
search_label.pack()
search_entry = tk.Entry(app, textvariable=search, font=("Segoe UI", 12), width=28)
search_entry.pack(pady=3)
search_entry.bind("<KeyRelease>", filter_tasks)

# Input field
entry = tk.Entry(app, font=("Segoe UI", 16), width=28, bd=2, relief="flat")
entry.pack(pady=10)

# Buttons
button_frame = tk.Frame(app, bg=bg_color)
button_frame.pack(pady=8)

buttons = [
    ("Add", add_task, "#4CAF50"),
    ("Delete", delete_task, "#FF3B30"),
    ("Edit", edit_task, "#FF9500"),
    ("Clear All", clear_all, "#C70039"),
    ("Theme", toggle_theme, "#00A8FF")
]

for i, (text, cmd, color) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=cmd, bg=color, fg="white",
              font=("Segoe UI", 12, "bold"), width=10, relief="flat").grid(row=0, column=i, padx=5)

# Task list + Scrollbar
frame = tk.Frame(app)
frame.pack(pady=15)

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(frame, width=45, height=16, font=("Segoe UI", 14),
                       selectbackground="#6A5ACD", activestyle="none",
                       yscrollcommand=scroll.set, bg="#333333", fg="white", bd=0)
task_list.pack(side=tk.LEFT, fill=tk.BOTH)
scroll.config(command=task_list.yview)

# Double click = mark task completed
task_list.bind("<Double-1>", mark_completed)

load_tasks()
app.mainloop()
