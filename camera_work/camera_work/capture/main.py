import cv2
import numpy as np
import os
import time
import tkinter as tk

still_time = 3  # Seconds to wait while still
def set_variable():
    # Get the selected choice and set the variable, default value is 3
    choice = float(still_time.get())
    
    if choice == 1:
        variable = "1 Second Selected"
    elif choice == 2:
        variable = "2 Seconds Selected"
    elif choice == 3:
        variable = "3 Seconds Selected"
    elif choice == 6:
        variable = "6 Seconds Selected"
    
    # Display the result in a label
    result_label.config(text=f"Variable set to: {variable}")

# Create the main window
root = tk.Tk()
root.title("Select how long you would like to be still before the hand sign is captured, then exit GUI")
root.state('zoomed')

# Create a variable to store the user's choice
still_time = tk.DoubleVar()

# Create radio buttons for different choices
tk.Radiobutton(root, text="1 second", variable=still_time, value=float(1.0)).pack(anchor=tk.W)
tk.Radiobutton(root, text="2 seconds", variable=still_time, value=float(2)).pack(anchor=tk.W)
tk.Radiobutton(root, text="3 seconds", variable=still_time, value=float(3)).pack(anchor=tk.W)
tk.Radiobutton(root, text="6 seconds", variable=still_time, value=float(6)).pack(anchor=tk.W)

# Create a button that triggers the variable setting
submit_button = tk.Button(root, text="Submit", command=set_variable)
submit_button.pack()

# Label to show the result
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

i = 1
still_threshold = 30  # Sensitivity: lower means more sensitive to motion
motion_counter = 0
start_time = None

# Get the first frame to use as reference
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert to grayscale and blur to reduce noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compute the absolute difference between the current frame and the previous one
    frame_diff = cv2.absdiff(prev_gray, gray)

    # Threshold the difference to find regions with significant changes (motion)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    motion_level = np.sum(thresh)  # Sum of differences, higher means more motion

    # Show the webcam feed
    cv2.imshow('Webcam Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    # Check if the motion is below the threshold for a certain period
    if motion_level < still_threshold:
        if start_time is None:
            start_time = time.time()  # Start counting still time
        elif time.time() - start_time >= float(still_time.get()):
            # If still for the set time, capture image
            image = f'images/captured_image{i}.jpg'
            cv2.imwrite(image, frame)
            print(f"Image captured and saved as '{image}'.")
            i += 1
            start_time = None  # Reset the still timer
    else:
        start_time = None  # Reset if motion is detected

    # Capture image if 'c' key is pressed manually
    if key == ord('c'):
        image = 'images/captured_image' + str(i) + '.jpg'
        cv2.imwrite(image, frame)
        print(f"Image captured and saved as '{image}'.")
        i += 1

    # Break the loop on 'q' key press
    if key == ord('q'):
        print(str(still_time.get()))
        break

    # Delete all captured images on 'd' key press
    if key == ord('d'):
        folder_path = r'images'

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
            i = 1
        else:
            print(f"The folder '{folder_path}' does not exist or is not a directory.")

    # Update the previous frame
    prev_gray = gray.copy()

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
