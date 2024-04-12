import tkinter as tk
from tkinter import filedialog
from Filesorting import *

selected_file_paths = []
selected_folders = []
directory = os.path.expanduser("~/Desktop")
selected_folders = get_folders(directory)

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        input_text.insert(tk.END, f"{file_path}\n")
        selected_file_paths.append(file_path)


def sort_files():
    for file_path in selected_file_paths:
        new_file_path = sort_file(file_path, selected_folders)
        output_text.insert(tk.END, f"{new_file_path}\n")


def get_text_height(text_widget):
    num_lines = int(text_widget.index('end-1c').split('.')[0])
    text_height = text_widget.winfo_reqheight()
    line_height = text_height / num_lines
    return line_height


root = tk.Tk()
root.title("File Sorting Tool")

# Set window size
root.geometry("1000x500")

# Dark Mode theme
root.configure(bg="#2C2F33")
root.option_add("*TButton*background", "#7289DA")
root.option_add("*TButton*foreground", "white")
root.option_add("*TLabel*background", "#2C2F33")
root.option_add("*TLabel*foreground", "white")
root.option_add("*TEntry*background", "white")
root.option_add("*TEntry*foreground", "black")

# Main frame
main_frame = tk.Frame(root, bg="#2C2F33")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Buttons frame
buttons_frame = tk.Frame(main_frame, bg="#2C2F33")
buttons_frame.grid(row=0, column=0, padx=10, pady=180, sticky="nsew")

# Sort button
sort_button_text = "Sort Files"

button_sort = tk.Button(buttons_frame, text=sort_button_text, font=("Arial", 12), width=12, command=sort_files)
button_sort.pack(side=tk.TOP,anchor=tk.CENTER, padx=5, pady=5)

# Input section
input_frame = tk.Frame(main_frame, bg="#2C2F33")
input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

input_label = tk.Label(input_frame, text="Select files to sort:", font=("Arial", 12), bg="#2C2F33", fg="white")
input_label.pack(pady=10)

# Select Button
button_select_file = tk.Button(buttons_frame, text="Select File",anchor=tk.CENTER, font=("Arial", 12),width=12, command=select_file)
button_select_file.pack(pady=5)

input_text = tk.Text(input_frame, height=20, width=40, font=("Arial", 12), bg="#36393F", fg="white")
input_text.pack(pady=10)

# Output section
output_frame = tk.Frame(main_frame, bg="#2C2F33")
output_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

output_label = tk.Label(output_frame, text="Output:", font=("Arial", 12), bg="#2C2F33", fg="white")
output_label.pack(pady=10)

output_text = tk.Text(output_frame, height=20, width=40, font=("Arial", 12), bg="#36393F", fg="white")
output_text.pack(pady=10)

root.mainloop()