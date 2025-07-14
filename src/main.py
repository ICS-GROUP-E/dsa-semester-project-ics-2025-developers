import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.gui_appl import IntegratedLibraryGUI

def main():
    app = IntegratedLibraryGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
