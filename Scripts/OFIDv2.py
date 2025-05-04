import os
import glob
import shutil
import pickle
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ======================
# ICON CONFIGURATION
# ======================
def set_window_icon(root):
    try:
        # Change this path to your icon file location
        icon_path = os.path.join(os.path.dirname(__file__), "Images", "hacker.ico")
        
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            # Fallback to default icon if custom icon not found
            root.iconbitmap(default='')  # This clears any default icon
    except Exception as e:
        print(f"Icon error: {str(e)}")  # Fails silently if icon can't be loaded

# ======================
# DARK THEME CONFIGURATION
# ======================
def configure_dark_theme(root):
    """Applies a consistent dark theme across all UI elements"""
    root.tk_setPalette(
        background='#222222',
        foreground='white',
        activeBackground='#444444',
        activeForeground='white'
    )
    
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure(
        '.',
        background='#222222',
        foreground='white',
        fieldbackground='#333333'
    )
    
    style.configure(
        'TButton',
        background='#444444',
        foreground='white',
        bordercolor='#555555'
    )
    
    style.map(
        'TButton',
        background=[('active', '#555555')]
    )

# ======================
# FILE ORGANIZATION LOGIC
# ======================
def organize_files(path):
    """Organizes files by extension"""
    undo_data = []
    try:
        # Record original locations
        for file in glob.glob(os.path.join(path, '*')):
            if os.path.isfile(file):
                undo_data.append(file)
        
        # Organize files
        for file in undo_data:
            ext = os.path.splitext(file)[1][1:] or "NO_EXT"
            target_dir = os.path.join(path, ext)
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(file, os.path.join(target_dir, os.path.basename(file)))
        
        # Save undo data
        with open(os.path.join(path, '.ofid_undo'), 'wb') as f:
            pickle.dump(undo_data, f)
            
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Organization failed:\n{str(e)}")
        return False

def undo_organization(path):
    """Undoes previous organization"""
    try:
        undo_file = os.path.join(path, '.ofid_undo')
        if not os.path.exists(undo_file):
            return False
            
        with open(undo_file, 'rb') as f:
            original_paths = pickle.load(f)
        
        # Move files back
        for original_path in original_paths:
            filename = os.path.basename(original_path)
            ext = os.path.splitext(filename)[1][1:] or "NO_EXT"
            current_path = os.path.join(path, ext, filename)
            
            if os.path.exists(current_path):
                shutil.move(current_path, original_path)
        
        # Clean up
        os.remove(undo_file)
        
        # Remove empty directories
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and not os.listdir(item_path):
                os.rmdir(item_path)
                
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Undo failed:\n{str(e)}")
        return False

# ======================
# MAIN APPLICATION GUI
# ======================
class OFIDApp:
    def __init__(self, root):
        self.root = root
        set_window_icon(root)  # Set custom icon
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("OFIDv2")
        self.root.geometry("500x300")
        configure_dark_theme(self.root)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(
            main_frame,
            text="OFIDv2 File Organizer",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 10))
        
        ttk.Label(
            main_frame,
            text="Organize files by extension automatically !",
            font=("Helvetica", 10)
        ).pack(pady=(0, 20))
        
        # Folder selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.folder_path = tk.StringVar()
        ttk.Label(folder_frame, text="Target Folder:").pack(anchor=tk.W)
        
        entry_frame = ttk.Frame(folder_frame)
        entry_frame.pack(fill=tk.X)
        
        ttk.Entry(entry_frame, textvariable=self.folder_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            entry_frame,
            text="Browse...",
            command=self.browse_folder,
            width=10
        ).pack(side=tk.RIGHT, padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(10, 20))
        
        ttk.Button(
            btn_frame,
            text="Organize Files",
            command=self.organize,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Undo Organization",
            command=self.undo,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Copyright notice - properly formatted
        copyright_frame = ttk.Frame(main_frame)
        copyright_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Base copyright text
        ttk.Label(
            copyright_frame,
            text="Copyrights © 2025 All Rights Reserved by $SecDev_Zakaria",
            font=("Helvetica", 8),
            foreground="gray70"
        ).pack(side=tk.LEFT)
        
        # Separator
        ttk.Label(
            copyright_frame,
            text=" | ",
            font=("Helvetica", 8),
            foreground="gray70"
        ).pack(side=tk.LEFT)

        # Clickable GitHub link
        github_link = ttk.Label(
            copyright_frame,
            text="GitHub ",
            font=("Helvetica", 8, "underline"),
            foreground="#00C834",  # GitHub Green
            cursor="hand2"
        )
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/BARI-Zakaria"))

        # Separator
        ttk.Label(
            copyright_frame,
            text=" | ",
            font=("Helvetica", 8),
            foreground="gray70"
        ).pack(side=tk.LEFT)
        
        # Clickable LinkedIn link
        github_link = ttk.Label(
            copyright_frame,
            text="LinkedIn",
            font=("Helvetica", 8, "underline"),
            foreground="#0A66C2",  # LinkedIn blue
            cursor="hand2"
        )
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/zakaria-bari/"))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            
            # Check for existing undo file
            undo_file = os.path.join(folder, '.ofid_undo')
            if os.path.exists(undo_file):
                messagebox.showinfo(
                    "Info", 
                    "This folder contains previous organization data.\n"
                    "You can use 'Undo Organization' to revert."
                )
    
    def organize(self):
        path = self.folder_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a folder first!")
            return
            
        if organize_files(path):
            messagebox.showinfo("Success", "Files organized successfully!")
    
    def undo(self):
        path = self.folder_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a folder first!")
            return
            
        if undo_organization(path):
            messagebox.showinfo("Success", "Organization undone successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OFIDApp(root)
    root.mainloop()