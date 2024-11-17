import sys
import os
import time

# Add the parent directory of 'cheat_detection' to the system path
sys.path.append(r"/Users/ayushgoel/OS Project/Cheat-Detection-System")

# Now you can import 'cheat_detection' correctly
from cheat_detection.monitor import GameMonitor  # Import the GameMonitor clas

def main():
    monitor = GameMonitor()  # Initialize GameMonitor
    print("Starting game monitoring...")

    try:
        while True:
            monitor.monitor_game_environment()  # Monitor for suspicious processes
            monitor.log_system_resources()  # Log CPU and memory usage
            time.sleep(5)  # Wait 5 seconds before next check

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")

if __name__ == "__main__":
    main()
