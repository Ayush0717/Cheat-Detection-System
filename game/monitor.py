import socket

# Set the maximum allowed speeds for detecting cheats
MAX_PLAYER_SPEED = 10  # Adjust as necessary
MAX_BULLET_SPEED = 12  # Adjust as necessary

def monitor():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("localhost", 9999))
        print("Monitoring script is running...")

        try:
            while True:
                data, addr = s.recvfrom(1024)
                if data:
                    # Decode the received data and split it into player speed and bullet speed
                    player_speed, bullet_speed = map(float, data.decode().split(','))
                    
                    # Print the received values
                    print(f"Received data: Player Speed = {player_speed}, Bullet Speed = {bullet_speed}")
                    
                    # Check if speeds exceed the maximum allowed thresholds
                    if player_speed > MAX_PLAYER_SPEED:
                        print("Warning: Cheat detected! Player speed exceeds limit.")
                    if bullet_speed > MAX_BULLET_SPEED:
                        print("Warning: Cheat detected! Bullet speed exceeds limit.")
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    monitor()
