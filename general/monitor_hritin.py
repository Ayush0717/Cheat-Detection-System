import socket

MAX_PLAYER_SPEED = 10 
MAX_BULLET_SPEED = 12 

def monitor():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("localhost", 9999))
        print("Monitoring script is running...")

        try:
            while True:
                data, addr = s.recvfrom(1024)
                if data:
                    message = data.decode()
                    player_speed, bullet_speed = map(float, message.split(','))

                    if player_speed == 100 and bullet_speed == 50:
                        print("ALERT: Cheat code injected into the game!")
                    else:
                        if player_speed == -1 and bullet_speed == -1:
                            print("ALERT: Player attempted to cheat by pressing the 'L' key to increase score!")
                        else:
                            print(f"Received data: Player Speed = {player_speed}, Bullet Speed = {bullet_speed}")

                        if player_speed > MAX_PLAYER_SPEED:
                            print("Warning: Cheat detected! Player speed exceeds limit.")
                        if bullet_speed > MAX_BULLET_SPEED:
                            print("Warning: Cheat detected! Bullet speed exceeds limit.")
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    monitor()
