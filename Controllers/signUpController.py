import os

import cv2
from PIL import Image, ImageTk
from tkinter import messagebox

from Views.signupView import SignUpView

class SignUpController:
    def __init__(self):
        self.view = SignUpView(self)
        self.camera_label = self.view.camera_label  # Assign camera label from the view

    def sign_up(self, first_name, last_name, matric_number, phone_number, department, level):
        # Do something with the collected information, such as saving to a database
        # For now, just print the information
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Matric Number:", matric_number)
        print("Phone Number:", phone_number)
        print("Department:", department)
        print("Level:", level)

        if first_name == "" or last_name == "" or matric_number == "" or department == "" or level == "":
            messagebox.showerror("Error", "Please fill in all the fields")
        else:
            self.display_camera()

    def display_camera(self):
        self.camera_open = True
        # Initialize the video capture object
        cap = cv2.VideoCapture(0)

        # Load the pre-trained face detection classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Variables to track the number of correctly detected faces and the total number of faces detected
        correct_faces = 0
        total_faces = 0

        # Function to update camera feed
        def update_camera_feed():
            nonlocal correct_faces, total_faces
            ret, frame = cap.read()
            if ret:
                # Convert OpenCV BGR frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # If only one face is detected and its area is larger than a threshold, save the image if accuracy >= 70 and stop camera feed
                if len(faces) == 1 and faces[0][2] * faces[0][3] > 10000:
                    x, y, w, h = faces[0]
                    # Take a picture of the detected face and save it
                    accuracy = (correct_faces / total_faces) * 100 if total_faces > 0 else 0
                    if accuracy >= 70:
                        face_img = frame_rgb[y:y + h, x:x + w]
                        folder_path = "faceDatabase"
                        os.makedirs(folder_path, exist_ok=True)
                        img_path = os.path.join(folder_path, "current.jpeg")
                        cv2.imwrite(img_path, cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
                        # Stop camera feed
                        cap.release()
                        self.camera_open = False
                        return

                    correct_faces += 1

                total_faces += len(faces)

                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Calculate and print the accuracy level
                accuracy = (correct_faces / total_faces) * 100 if total_faces > 0 else 0
                print("Accuracy:", accuracy, "%")

                # Convert frame to ImageTk format
                img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                # Update the label with the new frame
                self.camera_label.configure(image=img)
                self.camera_label.image = img
                # Schedule the next update after 10 milliseconds
                self.camera_label.after(10, update_camera_feed)
            else:
                # If camera feed cannot be captured, stop updating
                cap.release()

        # Start the camera feed update process
        update_camera_feed()
