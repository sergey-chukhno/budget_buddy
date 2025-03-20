import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the app package
from app.main_app import MainApp

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 