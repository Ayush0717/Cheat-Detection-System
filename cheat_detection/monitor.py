from cheat_detection.detector import CheatDetector
import time

class GameMonitor:
    def __init__(self, max_speed, min_bullet_interval, game_files):
        self.detector = CheatDetector(max_speed, min_bullet_interval, game_files)

    def monitor_player_speed(self, current_position):
        """Monitor player movement for speed hacks."""
        return self.detector.detect_speed_hack(current_position)

    def monitor_bullet_fire(self):
        """Monitor bullet firing for rapid fire."""
        current_time = time.time() * 1000  # Current time in milliseconds
        return self.detector.detect_rapid_fire(current_time)

    def monitor_file_integrity(self):
        """Monitor game file integrity."""
        return self.detector.check_file_integrity()
