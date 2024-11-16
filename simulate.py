import psutil
import os
import time
import threading
import subprocess

# Function to detect cheat activities
def detect_cheat():
    print("Cheat detection started...")
    while True:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        if memory_info.rss > 100 * 1024 * 1024:  # Example threshold for memory
            print("Illegal access detected: Excessive memory usage")
        
        for proc in psutil.process_iter(['pid', 'name']):
            if 'cheat' in proc.info['name'].lower() or 'x64' in proc.info['name'].lower():
                print(f"Illegal access detected: Suspicious process {proc.info['name']} (PID: {proc.info['pid']})")
        
        time.sleep(1)  # Pause to prevent continuous, non-stop checking

# Simulate memory manipulation by creating large data structures
def simulate_memory_manipulation():
    print("Simulating memory manipulation...")
    memory_hog = []
    while True:
        memory_hog.append(' ' * 1024 * 1024)  # Add 1MB chunks of space to the list
        time.sleep(0.1)

# Function to simulate suspicious process (mimicking a cheat tool)
def simulate_suspicious_process():
    print("Simulating suspicious process...")
    subprocess.Popen(["python3", "-c", "import time; time.sleep(1000)"])  # Simulate a process
    time.sleep(1)

# Start the cheat detection thread
cheat_detection_thread = threading.Thread(target=detect_cheat, daemon=True)
cheat_detection_thread.start()

# Start memory manipulation simulation thread
memory_simulation_thread = threading.Thread(target=simulate_memory_manipulation, daemon=True)
memory_simulation_thread.start()

# Start suspicious process simulation thread
suspicious_process_thread = threading.Thread(target=simulate_suspicious_process, daemon=True)
suspicious_process_thread.start()

# Keep the program running to allow threads to execute
while True:
    time.sleep(1)
