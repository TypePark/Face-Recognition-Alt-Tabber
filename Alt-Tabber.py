import cv2
import time
import platform # for detecting the operating system
import subprocess # makes code  able to use shell commands

def detect_faces():

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Load the pre-trained Haar Cascade classifier for face detection


    video_capture = cv2.VideoCapture(0) # Opens a connection to the webcam and select which one to use (0 is first cam)

    last_face_time = time.time()
    desktop_show_time = 5  # Shows desktop after 5 seconds of no face detection
    show_desktop_flag = False

    while True:

        ret_val, frame = video_capture.read() # Reads a frame from the webcam

        if not ret_val: #  for continuously detecting faces from the webcam
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converts the frame to grayscale for face detection


        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Detects faces in the frame


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # Draws rectangles around the detected faces


        cv2.imshow('Detected Faces', frame) # Display the frame with detected faces

        # If faces are detected, update the last_face_time and reset the show_desktop_flag
        if len(faces) > 0:
            last_face_time = time.time()
            show_desktop_flag = False
        else:
            # Checks if it's time to show the desktop
            if not show_desktop_flag and time.time() - last_face_time > desktop_show_time:
                show_desktop()
                show_desktop_flag = True

        # Exits the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Releases the video capture and closes the OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

def show_desktop():
    if platform.system() == "Windows":
        subprocess.run("explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}", shell=True) # special shell command that shows the desktop
    elif platform.system() == "Darwin":
        subprocess.run("osascript -e 'tell application \"System Events\" to key code 103 using control down'", shell=True)
    elif platform.system() == "Linux":
        subprocess.run("xdotool key super+d", shell=True)

if __name__ == "__main__": # for directly executing the Python file
    detect_faces()
