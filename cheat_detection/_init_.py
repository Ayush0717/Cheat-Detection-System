# Import classes from monitor.py and detector.py so that they are available at the package level
from .monitor import GameMonitor
from .detector import CheatDetector

# You can also assign them to the module level so that they can be accessed directly via the package
__all__ = ['GameMonitor', 'CheatDetector']
