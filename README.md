
# Rubik's Cube Solver

## Introduction
This Rubik's Cube Solver is a Python-based automated solution designed to solve a Rubik's Cube puzzle in the online simulator available at [Ruwix](https://ruwix.com/online-puzzle-simulators/). The program uses a combination of computer vision techniques and cube-solving algorithms to determine the cube's state and find the optimal solution.

## Requirements
- Python 3.x
- Libraries: `pyautogui`, `kociemba`, `cv2` (OpenCV), `numpy`, `Tkinter`
- Internet access to use the Ruwix online Rubik's Cube simulator

## Installation
To set up the Rubik's Cube Solver, follow these steps:

1. Clone or download the repository to your local machine.
2. Ensure Python 3.x is installed.
3. Install required Python libraries using pip:
   ```
   pip install pyautogui kociemba opencv-python numpy
   ```
4. Run the main script:
   ```
   python _main.py
   ```

## Usage
1. Open the [Ruwix Rubik's Cube Simulator](https://ruwix.com/online-puzzle-simulators/).
2. Start the Rubik's Cube Solver application.
3. Click the "Solve" button in the application.
4. The application will automatically solve the cube on the Ruwix simulator.

## Features
- **Automatic Cube Detection**: The program detects the current state of the Rubik's Cube.
- **Solving Algorithm**: Utilizes the Kociemba algorithm for efficient solving.
- **Interactive GUI**: Simple and user-friendly graphical interface with real-time status updates.

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Credits
Developed by Shehan.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
