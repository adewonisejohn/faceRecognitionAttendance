import os
import cv2

class FaceComparison:
    def __init__(self):
        print("about to get initialized")

    @staticmethod
    def compare_face(face, target):
        # Read images using OpenCV
        face_img = cv2.imread(f'faceDatabase/{face}.jpeg')
        target_img = cv2.imread(f'faceDatabase/{target}.jpeg')

        # Convert images to grayscale
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

        # Detect faces using Haar cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(face_gray, 1.1, 4)
        targets = face_cascade.detectMultiScale(target_gray, 1.1, 4)

        if len(faces) == 0 or len(targets) == 0:
            print("No faces detected in one or both images.")
            return False

        # Extract face regions and resize
        x, y, w, h = faces[0]
        face_roi = cv2.resize(face_gray[y:y+h, x:x+w], (128, 128))

        x, y, w, h = targets[0]
        target_roi = cv2.resize(target_gray[y:y+h, x:x+w], (128, 128))

        # Compute absolute difference
        diff = cv2.absdiff(face_roi, target_roi)
        mean_diff = diff.mean()

        # Set a threshold for similarity
        threshold = 30

        print("Mean difference:", mean_diff)

        # Compare faces based on the mean difference
        return mean_diff < threshold

    @staticmethod
    def check_face(face):
        return True
