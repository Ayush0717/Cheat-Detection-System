import time

def consume_memory():
    large_list = []
    while True:
        large_list.append(' ' * 10**6)  # Add 1MB chunks to the list
        time.sleep(1)  # Pause for 1 second

if __name__ == "__main__":
    consume_memory()
