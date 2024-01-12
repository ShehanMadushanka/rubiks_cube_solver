import pyautogui
import time
from PIL import Image
import numpy as np

def rotate_cube(rotation_sequence):
    for rotation in rotation_sequence:
        pyautogui.press(rotation)
        time.sleep(0.5)  # wait for the animation to complete

def capture_cube_state(file_name, region=None):
    time.sleep(1)  # wait for any cube rotation animation to finish
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(file_name)
    print(f"Captured {file_name}")

