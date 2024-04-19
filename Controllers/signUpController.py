import os
import sqlite3
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox

from Controllers.faceComparison import FaceComparison
from Model.signupModel import SignUpModel
from Views.signupView import SignUpView


class SignUpController:
    def __init__(self):
        # Initialize the database connection within a context manager
        with sqlite3.connect("attendance.db") as connection:
            self.connection = connection
            # Create the 'students' table if it doesn't exist
            cursor = self.connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS students (first_name TEXT, last_name TEXT, matric_number TEXT, department TEXT, level TEXT)")

        self.view = SignUpView(self)
        self.camera_label = self.view.camera_label  # Assign camera label from the view
        self.model = SignUpModel()

    def sign_up(self, first_name, last_name, matric_number, phone_number, department, level):
        # Do something with the collected information, such as saving to a database
        # For now, just print the information
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Matric Number:", matric_number)
        print("Phone Number:", phone_number)
        print("Department:", department)
        print("Level:", level)

        self.model.first_name = first_name
        self.model.last_name = last_name
        self.model.matric_number = matric_number
        self.model.department = department
        self.model.level = level

        if first_name == "" or last_name == "" or matric_number == "" or department == "" or level == "":
            messagebox.showerror("Error", "Please fill in all the fields")
        else:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM students WHERE matric_number = ?", (self.model.matric_number,))
            existing_student = cursor.fetchone()
            if existing_student:
                messagebox.showerror("Error", "A student with this information already exists")
            else:
                self.display_camera()

    def create_account(self):
        # Import SignInController here to avoid circular import
        from Controllers.signinController import SignInController

        # Check if the matric number already exists
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE matric_number = ?", (self.model.matric_number,))
        existing_student = cursor.fetchone()

        if existing_student:
            # If a student with the same matric number exists, show an error message
            messagebox.showerror("Error", "A student with this information already exists")
        else:
            isDetected  = FaceComparison.check_face(self.model.matric_number)
            if isDetected == True:
                cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                               (self.model.first_name, self.model.last_name, self.model.matric_number,
                                self.model.department, self.model.level))
                self.connection.commit()  # Commit the transaction
                messagebox.showinfo("Successful", "Profile created successfully")
                self.view.destroy()
                controller = SignInController()
                controller.view.mainloop()
            else:
                messagebox.showerror("Face not detected", "Make sure you have proper lighting and take off any facial wears")

    def display_camera(self):
        # Initialize variables to track face detection and camera status
        correct_faces = 0
        total_faces = 0
        camera_open = True

        # Initialize the video capture object
        cap = cv2.VideoCapture(0)

        # Load the pre-trained face detection classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Function to update camera feed
        def update_camera_feed():
            nonlocal correct_faces, total_faces, camera_open
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) == 1 and faces[0][2] * faces[0][3] > 10000:
                    x, y, w, h = faces[0]
                    accuracy = (correct_faces / total_faces) * 100 if total_faces > 0 else 0
                    if accuracy >= 30:
                        face_img = frame_rgb[y:y + h, x:x + w]
                        folder_path = "faceDatabase"
                        os.makedirs(folder_path, exist_ok=True)
                        img_path = os.path.join(folder_path, self.model.matric_number+".jpeg")
                        cv2.imwrite(img_path, cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
                        cap.release()
                        camera_open = False
                        self.create_account()
                        return
                    correct_faces += 1

                total_faces += len(faces)
                accuracy = (correct_faces / total_faces) * 100 if total_faces > 0 else 0
                for (x, y, w, h) in faces:
                    accuracy_text = f"Accuracy: {accuracy:.2f}%"
                    cv2.putText(frame_rgb, accuracy_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),
                                1)
                    cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

                print("Accuracy:", accuracy, "%")

                img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.camera_label.configure(image=img)
                self.camera_label.image = img
                self.camera_label.after(10, update_camera_feed)
            else:
                cap.release()

        # Start the camera feed update process
        update_camera_feed()
