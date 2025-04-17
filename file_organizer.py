import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

SUPPORTED_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt',
    '.heic', '.heif', '.mov', '.aae', '.livephoto', '.mp4', '.avi', '.mkv', '.wmv',
    '.flv', '.webm', '.mp3', '.wav', '.aac', '.ogg', '.opus', '.wma', '.m4a', '.zip', '.rar',
)

def organize_files(folder, mode, progress_callback=None):
    files = [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(SUPPORTED_EXTENSIONS)
    ]
    total = len(files)
    for idx, filename in enumerate(files, 1):
        file_path = os.path.join(folder, filename)
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        folder_name = mod_time.strftime('%Y-%m') if mode == 'Month' else mod_time.strftime('%Y')
        target_folder = os.path.join(folder, folder_name)
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(target_folder, filename))
        if progress_callback:
            progress_callback(idx, total)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y = self.widget.winfo_pointerxy()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x+10}+{y+10}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#222", foreground="#fff", relief=tk.SOLID, borderwidth=1,
            font=("Segoe UI", 9), padx=6, pady=2
        )
        label.pack()

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("480x360")
        self.minsize(480, 360)
        self.resizable(True, True)
        self.configure(bg="#f5f6fa")
        self.folder_path = tk.StringVar()
        self.mode = tk.StringVar(value="Month")
        self.status = tk.StringVar(value="Ready")
        self.progress = tk.IntVar(value=0)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TRadiobutton", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TProgressbar", thickness=20, troughcolor="#e1e2e6", background="#4caf50")
        style.map("TButton", background=[("active", "#4caf50"), ("pressed", "#388e3c")])
        style.map("TLabel", background=[("active", "#f5f6fa")])
        style.map("TEntry", background=[("active", "#fff")])
        style.map("TRadiobutton", background=[("active", "#f5f6fa")])
        style.map("TProgressbar", background=[("active", "#4caf50")])
        style.map("TProgressbar", troughcolor=[("active", "#e1e2e6")])

        title = ttk.Label(self, text="📁 File Organizer", font=("Segoe UI Semibold", 18), background="#f5f6fa", foreground="#222", anchor="center", justify="center")
        title.pack(pady=(18, 10), anchor="center")

        main_frame = ttk.Frame(self, padding=18)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=0)
        main_frame.rowconfigure(1, weight=0)
        main_frame.rowconfigure(2, weight=0)
        main_frame.rowconfigure(3, weight=0)
        main_frame.rowconfigure(4, weight=0)
        main_frame.rowconfigure(5, weight=1)

        folder_label = ttk.Label(main_frame, text="Select Folder:", anchor="center", justify="center")
        folder_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        folder_frame.columnconfigure(0, weight=1)
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=38, justify="center")
        folder_entry.grid(row=0, column=0, sticky="ew")
        browse_btn = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, width=9)
        browse_btn.grid(row=0, column=1, padx=(8, 0))
        ToolTip(browse_btn, "Choose the folder to organize")

        organize_label = ttk.Label(main_frame, text="Organize by:", anchor="center", justify="center")
        organize_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        mode_frame.columnconfigure(0, weight=1)
        mode_frame.columnconfigure(1, weight=1)
        month_rb = ttk.Radiobutton(mode_frame, text="Month", variable=self.mode, value="Month")
        year_rb = ttk.Radiobutton(mode_frame, text="Year", variable=self.mode, value="Year")
        month_rb.grid(row=0, column=0, padx=(0, 16), sticky="e")
        year_rb.grid(row=0, column=1, sticky="w")
        ToolTip(month_rb, "Organize files into folders by month (e.g., 2024-06)")
        ToolTip(year_rb, "Organize files into folders by year (e.g., 2024)")

        self.organize_btn = ttk.Button(main_frame, text="Organize", command=self.organize, width=16, state=tk.DISABLED)
        self.organize_btn.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        ToolTip(self.organize_btn, "Start organizing files")

        self.progressbar = ttk.Progressbar(main_frame, orient="horizontal", length=320, mode="determinate", variable=self.progress, maximum=100)
        self.progressbar.grid(row=5, column=0, columnspan=2, pady=(18, 0), sticky="ew")

        status_bar = ttk.Label(self, textvariable=self.status, anchor="center", background="#e1e2e6", font=("Segoe UI", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.folder_path.trace_add("write", self.on_folder_change)

    def on_folder_change(self, *args):
        folder = self.folder_path.get()
        state = tk.NORMAL if folder and os.path.isdir(folder) else tk.DISABLED
        self.organize_btn.config(state=state)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def organize(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        self.status.set("Organizing files...")
        self.organize_btn.config(state=tk.DISABLED)
        self.update_idletasks()
        self.progress.set(0)
        self.progressbar.update()
        files = [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(SUPPORTED_EXTENSIONS)
        ]
        total = len(files)
        if total == 0:
            self.status.set("No supported files found.")
            self.organize_btn.config(state=tk.NORMAL)
            return

        def progress_callback(idx, total):
            percent = int((idx / total) * 100)
            self.progress.set(percent)
            self.progressbar.update()
            self.status.set(f"Organizing... ({idx}/{total})")

        try:
            organize_files(folder, self.mode.get(), progress_callback)
            self.status.set("Files organized successfully!")
            self.progress.set(100)
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            self.status.set("Error occurred.")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            self.organize_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
