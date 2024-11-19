import game.psutil_scratch as psutil_scratch  # Used for monitoring processes
from cheat_detection.detector import CheatDetector

class GameMonitor:
    def __init__(self):
        self.detector = CheatDetector()
        
    def monitor_game_environment(self):
        """Monitor the game environment for any signs of cheating."""
        # Example: monitor running processes for cheating tools
        running_processes = psutil_scratch.process_iter(['pid', 'name'])
        for process in running_processes:
            if self.detector.is_suspicious(process):
                print(f"Suspicious activity detected: {process.name()} with PID {process.pid}")
                self.alert_player(process)
                
    def alert_player(self, process):
        """Alert player if suspicious activity is detected."""
        print(f"ALERT: Potential cheat detected! Process: {process.name()} PID: {process.pid}")
        # Here you can trigger actions like closing the game or notifying the player
