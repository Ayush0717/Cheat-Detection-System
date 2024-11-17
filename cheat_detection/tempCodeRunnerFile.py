import psutil  # Used for monitoring processes
from cheat_detection.detector import CheatDetector
import logging
import time

class GameMonitor:
    def __init__(self):
        self.detector = CheatDetector()
        self.suspicion_count = {}  # Track suspicious process counts
        self.suspicion_threshold = 3  # Threshold for taking action
        self.last_alert_time = {}  # Avoid spamming alerts
        logging.basicConfig(
            filename='cheat_detection_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("GameMonitor initialized.")
        
    def monitor_game_environment(self):
        """Monitor the game environment for any signs of cheating."""
        # Example: monitor running processes for cheating tools
        running_processes = psutil.process_iter(['pid', 'name'])
        for process in running_processes:
            if self.detector.is_suspicious(process):
                print(f"Suspicious activity detected: {process.name()} with PID {process.pid}")
                self.handle_suspicious_process(process)  # Handle suspicious processes
                
    def alert_player(self, process):
        """Alert player if suspicious activity is detected."""
        alert_message = f"ALERT: Potential cheat detected! Process: {process.name()} PID: {process.pid}"
        print(alert_message)
        logging.info(alert_message)
        # Here you can trigger actions like closing the game or notifying the player
    

    def handle_suspicious_process(self, process):
        """Handle suspicious process logic."""
        process_id = process.pid
        process_name = process.name()
        current_time = time.time()

        # Track suspicion count
        if process_id not in self.suspicion_count:
            self.suspicion_count[process_id] = 0

        self.suspicion_count[process_id] += 1

        # Avoid spamming alerts
        if process_id not in self.last_alert_time or current_time - self.last_alert_time[process_id] > 10:
            if self.suspicion_count[process_id] >= self.suspicion_threshold:
                self.alert_player(process)
                self.last_alert_time[process_id] = current_time

    def display_warning_overlay(self, process):
        """Show a non-intrusive warning overlay."""
        print(f"WARNING: {process.name()} (PID: {process.pid}) is flagged as suspicious.")
        logging.info(f"Warning overlay displayed for process {process.name()} with PID {process.pid}.")

    def log_system_resources(self):
        """Log system resource usage to detect anomalies."""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Log high resource usage
        if cpu_usage > 80:
            logging.warning(f"High CPU usage detected: {cpu_usage}%")
        if memory_info.percent > 90:
            logging.warning(f"High memory usage detected: {memory_info.percent}%")
