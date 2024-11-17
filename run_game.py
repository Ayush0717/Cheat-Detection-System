import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath("/Users/ayushgoel/OS Project/Cheat-Detection-System/run_game.py"))
sys.path.append(project_root)

# Import and run the game and monitor
from game.game_ayush import *
from cheat_detection.run_monitor import *  

