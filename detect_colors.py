import cv2
import numpy as np

# Define the RGB color codes for the Rubik's cube colors
cube_colors = {
    'green': np.array([1, 157, 85]),
    'orange': np.array([232, 112, 0]),
    'yellow': np.array([245, 180, 1]),
    'red': np.array([220, 66, 47]),
    'blue': np.array([61, 129, 246]),
    'white': np.array([243, 243, 243])
}


# Function to identify the color of a square based on its average color
def identify_square_color(average_rgb, color_codes):
    # Calculate the Euclidean distance between the average color and predefined colors
    distances = {color: np.linalg.norm(average_rgb - code) for color, code in color_codes.items()}
    # Find the minimum distance and corresponding color
    identified_color = min(distances, key=distances.get)
    return identified_color

# Function to apply perspective warp and process the cube face
def warp_and_process_cube_face(image, file_name):
    # The provided corner coordinates for the Rubik's cube front face
    cube_corners = np.array(corners, dtype="float32")

    # The output square dimensions
    output_size = 300
    # Destination points to map the input coordinates to a square
    destination_corners = np.array([
        [0, 0],
        [0, output_size - 1],
        [output_size - 1, output_size - 1],
        [output_size - 1, 0]
    ], dtype="float32")

    # Calculate the perspective transform matrix and apply the warp
    perspective_transform_matrix = cv2.getPerspectiveTransform(cube_corners, destination_corners)
    warped_image = cv2.warpPerspective(image, perspective_transform_matrix, (output_size, output_size))

    # Convert to RGB since OpenCV loads images in BGR
    warped_image_rgb = cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB)

    # Size of the image
    h, w = warped_image_rgb.shape[:2]
    square_size = h // 3
    border_size = square_size // 5  # Define a border to avoid including edges

    # Initialize the 3x3 matrix to hold the identified colors
    identified_colors = [['none' for _ in range(3)] for _ in range(3)]

    # Loop over each square and identify its color
    for i in range(3):
        for j in range(3):
            # Calculate the boundaries of the square (with a border to avoid the edges)
            x_start = j * square_size + border_size
            y_start = i * square_size + border_size
            x_end = (j + 1) * square_size - border_size
            y_end = (i + 1) * square_size - border_size

            # Compute the average color of the square within the border
            square_avg_color = np.mean(warped_image_rgb[y_start:y_end, x_start:x_end], axis=(0, 1))

            # Identify the color of the square
            identified_colors[i][j] = identify_square_color(square_avg_color, cube_colors)

    return identified_colors

# Function to detect the center colors of each face
def detect_center_colors(image, corners):
    # The provided corner coordinates for the Rubik's cube front face
    cube_corners = np.array(corners, dtype="float32")

    # The output square dimensions
    output_size = 300
    # Destination points to map the input coordinates to a square
    destination_corners = np.array([
        [0, 0],
        [0, output_size - 1],
        [output_size - 1, output_size - 1],
        [output_size - 1, 0]
    ], dtype="float32")

    # Calculate the perspective transform matrix and apply the warp
    perspective_transform_matrix = cv2.getPerspectiveTransform(cube_corners, destination_corners)
    warped_image = cv2.warpPerspective(image, perspective_transform_matrix, (output_size, output_size))

    # Convert to RGB since OpenCV loads images in BGR
    warped_image_rgb = cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB)

    # Size of the image
    h, w = warped_image_rgb.shape[:2]
    square_size = h // 3
    border_size = square_size // 5  # Define a border to avoid including edges

    # Calculate the center square coordinates
    center_x = output_size // 2
    center_y = output_size // 2
    border_size = output_size // 10  # smaller border for center square

    # Compute the average color of the center square
    center_avg_color = np.mean(
        warped_image_rgb[
            center_y-border_size:center_y+border_size,
            center_x-border_size:center_x+border_size
        ],
        axis=(0, 1)
    )

    # Identify the color of the center square
    center_color = identify_square_color(center_avg_color, cube_colors)

    return center_color

# Corners for the front face of the cube (assumed to be known)
corners = [
    [267, 246],  # Top-left corner
    [281, 549],  # Bottom-left corner
    [495, 649],  # Bottom-right corner
    [493, 303]   # Top-right corner
]
