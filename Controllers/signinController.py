import tkinter as tk
from tkinter import messagebox

import cv2
from PIL import Image, ImageTk
import os

from Controllers.signUpController import SignUpController
from Model.signinModel import SignInModel
from Views.signinView import SignInView

class SignInController:
    camera_open = False

    def __init__(self):
        self.model = SignInModel()
        self.view = SignInView(self)

        # Initialize the camera label
        self.camera_label = tk.Label(self.view.right_container)
        self.camera_label.pack()

    def sign_in(self):
        self.model.matric_number = self.view.matric_entry.get()
        self.model.course_code = self.view.course_entry.get()
        if self.model.matric_number == "" or self.model.course_code == "":
            messagebox.showerror("Invalid Credentials", "Please fill in the required information")
        else:
            print("Matric Number:", self.model.matric_number)
            print("Course Code:", self.model.course_code)
            # Display the camera feed after sign-in button is clicked
            if not self.camera_open:
                self.display_camera()

    def open_sign_up_page(self):
        self.view.destroy()
        SignUpController()
       # You can implement the functionality to open the sign-up page here

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
