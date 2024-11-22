import time
import threading

# Define a lock to protect shared data
shared_data_lock = threading.Lock()

# Shared data
shared_value = 0

# Define the function for task A
def main_loop():
    global shared_value
    while True:
        with shared_data_lock:
            print(f"Task A is running with shared_value: {shared_value}")
            # Modify shared data if needed
            shared_value += 1
        time.sleep(.2)

# Define the function for task B
def music(command):
    global shared_value
    with shared_data_lock:
        print(f"Task B is running with command: {command}")
        # Modify shared data if needed
        shared_value += 1

# Create a thread for task A
thread_a = threading.Thread(target=main_loop)
thread_a.daemon = True
thread_a.start()

# Main loop for user input
while True:
    user_input = input("Enter a command (or press Enter to continue task A): ")
    if user_input:
        # A command was entered, so run task B
        thread_b = threading.Thread(target=music, args=(user_input,))
        thread_b.start()
    # Continue with task A in the main thread
