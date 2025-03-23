import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main_app import MainApp

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 