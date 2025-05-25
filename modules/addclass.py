import tkinter as tk
from tkinter import ttk


def clear_fields():
    course_combobox.set('')
    year_section_combobox.set('')
    subject_code_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)


def add_class():
    course = course_combobox.get()
    year_section = year_section_combobox.get()
    subject_code = subject_code_entry.get()
    time = time_entry.get()

    print(f"Class Added: {course}, {year_section}, {subject_code}, {time}")


root = tk.Tk()
root.title("Class Management")
root.geometry("400x300")


course_label = tk.Label(root, text="Course")
course_label.pack(pady=5)
course_combobox = ttk.Combobox(root, values=["BS Computer Engineering"])
course_combobox.pack(pady=5)


year_section_label = tk.Label(root, text="Year & Section")
year_section_label.pack(pady=5)
year_section_combobox = ttk.Combobox(root, values=["1-5"])
year_section_combobox.pack(pady=5)


subject_code_label = tk.Label(root, text="Subject Code")
subject_code_label.pack(pady=5)
subject_code_entry = tk.Entry(root)
subject_code_entry.pack(pady=5)


time_label = tk.Label(root, text="Time")
time_label.pack(pady=5)
time_entry = tk.Entry(root)
time_entry.pack(pady=5)


clear_button = tk.Button(root, text="Clear", command=clear_fields, bg='red', fg='white')
clear_button.pack(side=tk.LEFT, padx=10, pady=20)

add_class_button = tk.Button(root, text="Add Class", command=add_class, bg='green', fg='white')
add_class_button.pack(side=tk.RIGHT, padx=10, pady=20)

root.mainloop()