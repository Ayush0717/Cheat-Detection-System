import time
import os

class CheatDetector:
    def __init__(self, max_speed, min_bullet_interval, game_files):
        self.max_speed = max_speed  # Maximum allowed player speed
        self.min_bullet_interval = min_bullet_interval  # Minimum allowed time between bullets
        self.game_files = game_files  # List of game files for integrity check
        self.last_bullet_time = 0  # Track the last bullet fired time

    def detect_speed_hack(self, current_position):
        """Detect speed hacks based on player movement."""
        # Assuming current_position is a tuple (x, y)
        # Check if the distance moved in a short time is above max_speed (simplified for now)
        x, y = current_position
        # Example of calculating movement speed (you can improve this based on actual game mechanics)
        speed = (x**2 + y**2)**0.5
        if speed > self.max_speed:
            return True  # Speed hack detected
        return False

    def detect_rapid_fire(self, current_time):
        """Detect rapid fire based on bullet firing interval."""
        # Check if the time between the current shot and the last shot is smaller than the minimum allowed interval
        if current_time - self.last_bullet_time < self.min_bullet_interval:
            return True  # Rapid fire detected
        self.last_bullet_time = current_time  # Update last bullet fired time
        return False

    def check_file_integrity(self):
        """Check game file integrity by comparing hashes or timestamps of important game files."""
        for file in self.game_files:
            if not os.path.exists(file):
                return False  # File missing or altered
            # Additional integrity checks could be implemented, like comparing hashes, file size, etc.
        return True  # All files are intact
