import pyautogui
import kociemba
import time
import detect_colors as dc
import cube_capture as cc
import cv2
import os
import tkinter as tk
from threading import Thread


def on_solve_click():
    """
    Function to be called when the Solve button is clicked.
    This should start the Rubik's Cube solving process in a separate thread to keep the GUI responsive.
    The status label should be updated accordingly within this function.
    """
    time.sleep(3)
    
    status_label.config(text="Reading Cube Faces...")
    
    cube_region = (2079, 187, 992, 797)
    side_names = ["front", "up", "right", "back", "left", "down"]
    side_symbols = {"front":"F", "up":"U", "right":"R", "back":"B", "left":"L", "down":"D"}
    saved_images = [f"cube_{side}.png" for side in side_names]
    rotation_sequences = {
        "front": [],  # No rotation needed; white is already at the front
        "up": ['x'],  # Rotate to bring orange (currently on top) to the front
        "right": ['X','Y'],  # Rotate to bring blue (right of white in your setup) to the front
        "back": ['y','y','y'],  # Rotate to bring yellow (opposite of orange) to the front
        "left": ['y','y','y'],  # Rotate to byring green (left of white in your setup) to the front
        "down": ['Y', 'X']  # Rotate to bring red (bottom of white in your setup) to the front
    }
    
    cube_faces_colors = {}

     # Ensure the first screenshot is taken before any rotations
    file_name = "cube_front.png"
    cc.capture_cube_state(file_name, region=cube_region)
    image = cv2.imread(file_name)
    colors = dc.warp_and_process_cube_face(image, "front")
    cube_faces_colors["front"] = colors

    # Now proceed with capturing and processing the other faces
    for side in side_names[1:]:  # Start from the second element
        if side in rotation_sequences:
            cc.rotate_cube(rotation_sequences[side])

        file_name = f"cube_{side}.png"
        cc.capture_cube_state(file_name, region=cube_region)
        image = cv2.imread(file_name)
        colors = dc.warp_and_process_cube_face(image, side)
        cube_faces_colors[side] = colors
        
    cc.rotate_cube({"x":['x']})  # Rotate back to the initial state
    
    initial_state_images = {}
    for side in side_names:
        file_name = f"cube_{side}.png"
        image = cv2.imread(file_name)
        initial_state_images[side_symbols[side]] = image
        
    current_orientation = {}
    for symbol, image in initial_state_images.items():
        center_color = dc.detect_center_colors(image, dc.corners)
        current_orientation[center_color] = symbol
        
    print(f"Current Color Map: {current_orientation}") 
    
    # Encode the colors for the solveryyy
    cube_string = encode_colors_for_solver(cube_faces_colors, current_orientation)
    
    print(f"cubestring: {cube_string}")
    
    delete_saved_images(saved_images)

    # # Solve the cube and get the solution moves
    solution_moves = kociemba.solve(cube_string)
    
    status_label.config(text="Solving...")

    # # Execute the solution moves
    execute_solution(solution_moves)
    
    status_label.config(text="Done!")
    
def start_solve():
    """
    Starts the solving process in a separate thread to keep the GUI responsive.
    """
    solving_thread = Thread(target=on_solve_click)
    solving_thread.start()

# Function to encode the colors into the cube string format for the solver
def encode_colors_for_solver(cube_faces_colors, color_map):
    # Convert the face colors to the solver's string format
    cube_string = ''
    for face in ['up', 'right', 'front', 'down', 'left', 'back']:
        for color_row in cube_faces_colors[face]:
            for color in color_row:
                cube_string += color_map[color]
                print(face, color, color_map[color])

    return cube_string

# Function to execute the solution moves
def execute_solution(solution_moves):
    for move in solution_moves.split():
        # Check if the move is a prime move (counter-clockwise), indicated by an apostrophe
        if move.endswith("'"):
            # Send the lowercase letter of the move (counter-clockwise rotation)
            pyautogui.press(move[0].lower())
        elif move.endswith("2"):
            # For double moves, press the key twice
            pyautogui.press(move[0])
            pyautogui.press(move[0])
        else:
            # Send the uppercase letter of the move (clockwise rotation)
            pyautogui.press(move)
        time.sleep(0.5)  # Wait for the move to complete
        
# Function to delete saved images
def delete_saved_images(image_paths):
    for image_path in image_paths:
        try:
            os.remove(image_path)
            print(f"Deleted {image_path}")
        except OSError as e:
            print(f"Error deleting {image_path}: {e.strerror}")

# Main workflow
# Create the main window
root = tk.Tk()
root.title("Rubik's Cube Challenge")
root.geometry("300x150")
root.attributes("-topmost", True)

# Create a status label
status_label = tk.Label(root, text="Ready", font=("Arial", 12))
status_label.pack(pady=10)

# Create a Solve button
solve_button = tk.Button(root, text="Solve", command=start_solve)
solve_button.pack(pady=10)

name_label = tk.Label(root, text="Powered by Shehan", font=("Arial", 12))
name_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()   
