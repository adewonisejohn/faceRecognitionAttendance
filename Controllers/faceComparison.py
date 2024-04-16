import os
import face_recognition

class FaceComparison:
    def __init__(self):
        print("about to get initialized")

    @staticmethod
    def compare_face(face, target):
        folder_path = "faceDatabase"
        os.makedirs(folder_path, exist_ok=True)

        known_image = face_recognition.load_image_file(os.path.join(folder_path, f'{face}.jpeg'))
        unknown_image = face_recognition.load_image_file(os.path.join(folder_path, f'{target}.jpeg'))

        # Encode faces
        known_encoding = face_recognition.face_encodings(known_image)
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        # Check if encodings are found
        if not known_encoding:
            print(f"No face found in the image: {face}")
            return False
        if not unknown_encoding:
            print(f"No face found in the image: {target}")
            return False

        # Calculate face distances
        face_distance = face_recognition.face_distance(known_encoding, unknown_encoding[0])

        # Check if face distance is within tolerance
        tolerance = 0.6  # Adjust the tolerance level as needed
        if face_distance <= tolerance:
            print(f"Face match with distance: {face_distance}")
            return True
        else:
            print(f"Face does not match with distance: {face_distance}")
            return False

    def check_face(face):
        folder_path = "faceDatabase"
        os.makedirs(folder_path, exist_ok=True)

        known_image = face_recognition.load_image_file(os.path.join(folder_path, f'{face}.jpeg'))
        known_encoding = face_recognition.face_encodings(known_image)

        if known_encoding:
            return True;
        else:
            os.remove(os.path.join(folder_path, f'{face}.jpeg'))
            return False

