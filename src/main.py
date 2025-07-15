import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import subprocess
import importlib

def install_requirements():
    """Install required packages from requirements.txt if they're missing."""
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
    
    try:
        print("Checking and installing requirements...")
        # Just try to install everything - pip will skip already installed packages
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("All required packages have been installed successfully!")
        return True
    except Exception as e:
        print(f"Error installing requirements: {str(e)}")
        try:
            # Try to show error in GUI if possible
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Installation Error", 
                               f"Failed to install required packages.\nError: {str(e)}\n\nPlease run: pip install -r requirements.txt")
            root.destroy()
        except:
            # If GUI fails, just print to console
            pass
        return False

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # First check and install requirements
    if install_requirements():
        try:
            from ui.gui_appl import IntegratedLibraryGUI
            app = IntegratedLibraryGUI()
            app.mainloop()
        except Exception as e:
            print(f"Error starting application: {str(e)}")
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Error", f"Failed to start application.\nError: {str(e)}")
                root.destroy()
            except:
                # If GUI fails, error was already printed to console
                pass

if __name__ == "__main__":
    main()
