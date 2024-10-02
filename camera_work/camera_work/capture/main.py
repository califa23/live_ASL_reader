import cv2
import os

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
i = 1
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('Webcam Feed', frame)
    key = cv2.waitKey(1) & 0xFF

    # Capture image if 'c' key is pressed
    if key == ord('c'):
        image = 'images/captured_image' + str(i) + '.jpg'
        cv2.imwrite(image, frame)
        print("Image captured and saved as '" + image + "'.")
        i+=1

    # Break the loop on 'q' key press
    if key == ord('q'):
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
        

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()