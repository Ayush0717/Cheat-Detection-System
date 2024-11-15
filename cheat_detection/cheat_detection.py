import socket
import time

# Set up server to listen for game data
server_ip = "127.0.0.1"
server_port = 8080

def detect_cheat(data):
    # Simulate a basic cheat detection process
    # Example checks for abnormal movement or high bullet count
    player_data = data.split(',')
    player_x, player_y, bullet_count = int(player_data[0]), int(player_data[1]), int(player_data[2])
    
    # Check for abnormal player position (out of bounds)
    if player_x < 0 or player_x > 800 or player_y < 0 or player_y > 600:
        return "Anomaly Detected: Player out of bounds"
    
    # Check for unusually high bullet count
    if bullet_count > 100:
        return "Anomaly Detected: Too many bullets fired"
    
    # No anomalies detected
    return "No Anomaly Detected"

def start_cheat_detection_server():
    # Set up the server to listen for data from the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)

    print(f"Cheat Detection System is running on {server_ip}:{server_port}")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Receive data from the game
        data = conn.recv(1024).decode("utf-8")
        print(f"Received data: {data}")
        
        # Check if there's an anomaly
        result = detect_cheat(data)
        
        # Send back the result to the game
        conn.send(result.encode("utf-8"))
        conn.close()

# Start the cheat detection system
if __name__ == "__main__":
    start_cheat_detection_server()
