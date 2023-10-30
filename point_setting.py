
from pynput.mouse import Listener
import keyboard

# Function to handle mouse click events
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Clicked at coordinates: ({x}, {y})")

# Function to stop the program when the Home key is pressed
def stop_program(e):
    if e.name == "home":
        listener.stop()

# Register a keyboard event listener for the Home key
keyboard.on_press(stop_program)

# Create a mouse listener
with Listener(on_click=on_click) as listener:
    print("Listening for mouse clicks. Press Home to exit.")
    listener.join()
