import psutil

class CheatDetector:
    def __init__(self):
        # Example of a list of known cheat tools or suspicious processes
        self.suspicious_processes = ['cheatengine', 'exploittool', 'hacktool']
        
    def is_suspicious(self, process):
        """Check if the process is suspicious based on predefined conditions."""
        return any(suspicious_name in process.name().lower() for suspicious_name in self.suspicious_processes)
