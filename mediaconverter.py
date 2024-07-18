import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import threading

class MediaConverter:
    def __init__(self, master):
        self.master = master
        master.title("Media Converter")

        # Input Format Dropdown
        input_label = tk.Label(master, text="Input Format:")
        input_label.grid(row=0, column=0, padx=5, pady=5)

        self.input_formats = ["mp3", "ogg", "wav", "m4a", "aac"]  # Add more formats as needed
        self.input_var = tk.StringVar(master)
        self.input_var.set(self.input_formats[0])  # Default format
        input_dropdown = ttk.Combobox(master, textvariable=self.input_var, values=self.input_formats)
        input_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Output Format Dropdown
        output_label = tk.Label(master, text="Output Format:")
        output_label.grid(row=1, column=0, padx=5, pady=5)

        self.output_formats = ["flac", "m4a", "mp3", "wav", "aac"]  # Add more formats as needed
        self.output_var = tk.StringVar(master)
        self.output_var.set(self.output_formats[0])  # Default format
        output_dropdown = ttk.Combobox(master, textvariable=self.output_var, values=self.output_formats)
        output_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Input File Selection Button
        input_file_button = tk.Button(master, text="Select Input File", command=self.select_input_file)
        input_file_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Convert Button
        convert_button = tk.Button(master, text="Convert", command=self.convert_media)
        convert_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Attributes
        self.input_file = None
        self.progress_var = tk.DoubleVar(value=0)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(
            initialdir="/",
            title="Select Input File",
            filetypes=(("All Files", "*.*"),)
        )

    def convert_media(self):
        if not self.input_file:
            tk.messagebox.showerror("Error", "Please select an input file.")
            return

        input_format = self.input_var.get()
        output_format = self.output_var.get()

        # Construct ffmpeg command
        command = [
            "ffmpeg",
            "-i",
            self.input_file,
            "-vn",  # Disable video stream
            "-acodec", output_format,
            f"{self.input_file[:-len(input_format)]}.{output_format}"
        ]

        # Create a thread for ffmpeg execution (to avoid blocking the GUI)
        def run_ffmpeg():
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                while True:
                    output, error = process.communicate()
                    if process.poll() is not None:
                        break
                    self.progress_var.set(process.poll())
                    self.master.update_idletasks()  # Update the GUI
            except Exception as e:
                tk.messagebox.showerror("Error", f"Conversion failed: {e}")

        convert_thread = threading.Thread(target=run_ffmpeg)
        convert_thread.start()

# Create the main window and run the application
root = tk.Tk()
app = MediaConverter(root)
root.mainloop()