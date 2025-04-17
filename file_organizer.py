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
        if mode == 'Month':
            folder_name = mod_time.strftime('%Y-%m')
        else:
            folder_name = mod_time.strftime('%Y')
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
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, "bbox") else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#222", foreground="#fff", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", 9, "normal"), padx=6, pady=2)
        label.pack()

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("480x320")
        self.resizable(False, False)
        self.configure(bg="#f5f6fa")
        self.folder_path = tk.StringVar()
        self.mode = tk.StringVar(value="Month")
        self.status = tk.StringVar(value="Ready")
        self.progress = tk.IntVar(value=0)
        self.total_files = 1
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TEntry", font=("Segoe UI", 11))
        style.configure("TRadiobutton", background="#f5f6fa", font=("Segoe UI", 11))

        title = ttk.Label(self, text="📁 File Organizer", font=("Segoe UI Semibold", 18), background="#f5f6fa", foreground="#222")
        title.pack(pady=(18, 10))

        main_frame = ttk.Frame(self, padding=18)
        main_frame.pack(fill=tk.BOTH, expand=True)

        folder_label = ttk.Label(main_frame, text="Select Folder:")
        folder_label.grid(row=0, column=0, sticky="w", pady=(0, 8))
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=38, font=("Segoe UI", 11))
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        browse_btn = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, width=9)
        browse_btn.pack(side=tk.LEFT, padx=(8, 0))
        ToolTip(browse_btn, "Choose the folder to organize")

        organize_label = ttk.Label(main_frame, text="Organize by:")
        organize_label.grid(row=2, column=0, sticky="w", pady=(0, 8))
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 12))
        month_rb = ttk.Radiobutton(mode_frame, text="Month", variable=self.mode, value="Month")
        year_rb = ttk.Radiobutton(mode_frame, text="Year", variable=self.mode, value="Year")
        month_rb.pack(side=tk.LEFT, padx=(0, 16))
        year_rb.pack(side=tk.LEFT)
        ToolTip(month_rb, "Organize files into folders by month (e.g., 2024-06)")
        ToolTip(year_rb, "Organize files into folders by year (e.g., 2024)")

        self.organize_btn = ttk.Button(main_frame, text="Organize", command=self.organize, width=16, state=tk.DISABLED)
        self.organize_btn.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ToolTip(self.organize_btn, "Start organizing files")

        self.progressbar = ttk.Progressbar(main_frame, orient="horizontal", length=320, mode="determinate", variable=self.progress, maximum=100)
        self.progressbar.grid(row=5, column=0, columnspan=2, pady=(18, 0))

        # Status bar
        status_bar = ttk.Label(self, textvariable=self.status, anchor="w", background="#e1e2e6", font=("Segoe UI", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind folder path changes to enable/disable organize button
        self.folder_path.trace_add("write", self.on_folder_change)

    def on_folder_change(self, *args):
        folder = self.folder_path.get()
        if folder and os.path.isdir(folder):
            self.organize_btn.config(state=tk.NORMAL)
        else:
            self.organize_btn.config(state=tk.DISABLED)

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
