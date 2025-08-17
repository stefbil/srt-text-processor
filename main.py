import tkinter as tk
from tkinter import filedialog, messagebox
import unicodedata
import os

def process_text(input_text: str) -> str:
    """Removes accents, commas, and periods from a string."""
    text_no_accents = unicodedata.normalize('NFD', input_text)
    text_no_accents = "".join(c for c in text_no_accents if unicodedata.category(c) != 'Mn')
    final_text = text_no_accents.replace(',', '').replace('.', '')
    return final_text

# --- GUI Application Functions ---

def select_file():
    """Opens a dialog to select an SRT file and updates the label."""
    filepath = filedialog.askopenfilename(
        title="Select a Greek SRT File",
        filetypes=(("SRT files", "*.srt"), ("All files", "*.*"))
    )
    if filepath:
        filepath_label.config(text=filepath)

# --- MODIFIED FUNCTION TO PROCESS FILE CORRECTLY ---
def process_and_save_file():
    """Processes only the subtitle text lines in the selected SRT file."""
    input_path = filepath_label.cget("text")

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Please select a valid SRT file first.")
        return

    base_name, extension = os.path.splitext(input_path)
    output_path = f"{base_name}_processed{extension}"

    try:
        # Open both files at once
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:

            # Read the file line by line
            for line in infile:
                # Identify timestamp lines (they contain '-->')
                # and sequence number lines (they are just digits).
                is_timestamp = '-->' in line
                is_sequence_number = line.strip().isdigit()

                if is_timestamp or is_sequence_number:
                    # If it's a timestamp or number, write it to the new file without changes.
                    outfile.write(line)
                else:
                    # Otherwise, it's a subtitle text line or a blank line.
                    # Process this line to remove accents and punctuation.
                    processed_line = process_text(line)
                    outfile.write(processed_line)
        
        messagebox.showinfo("Success", f"File processed successfully!\nSaved as: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# --- GUI Setup (No changes here) ---

root = tk.Tk()
root.title("SRT Text Processor")
root.geometry("500x200")

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(expand=True)

select_button = tk.Button(frame, text="1. Select SRT File", command=select_file)
select_button.pack(fill='x', pady=5)

filepath_label = tk.Label(frame, text="No file selected", wraplength=450, fg="gray")
filepath_label.pack(pady=5)

process_button = tk.Button(frame, text="2. Process and Save", command=process_and_save_file)
process_button.pack(fill='x', pady=10)

root.mainloop()