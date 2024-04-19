import os
import tkinter as tk
from tkinter import simpledialog
import subprocess

class SignInView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Sign In")
        self.geometry("1000x600")  # Set window size

        # Left container with a deeper background color
        self.left_container = tk.Frame(self, bg="#BFBFBF")  # Set background color to a deeper shade
        self.left_container.pack(side="left", fill="both", expand=False, padx=10, pady=10)  # Add padding

        # Left container widgets
        entry_font = ("IBM Plex Sans", 30)  # Set font family to IBM Plex Sans
        entry_bg = "white"  # Set background color to a deeper shade
        entry_fg = "black"  # Set entry text color to black
        label_fg = "#666666"  # Set label text color to grey
        label_font = ("IBM Plex Sans", 15, "bold")  # Set label font to bold

        self.matric_label = tk.Label(self.left_container, text="Matric Number:", fg=label_fg, bg="#BFBFBF", font=label_font)  # Set background color to a deeper shade
        self.matric_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))  # Align top-left and add padding

        self.matric_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg, font=entry_font)  # Remove highlightthickness=0
        self.matric_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))  # Expand to fill horizontally, add padding

        self.course_label = tk.Label(self.left_container, text="Course Code:", fg=label_fg, bg="#BFBFBF", font=label_font)  # Set background color to a deeper shade
        self.course_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))  # Align top-left and add padding

        self.course_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg, font=entry_font)  # Remove highlightthickness=0
        self.course_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 5))  # Expand to fill horizontally, add padding

        # Sign-in button with increased height and no outline
        button_font = ("IBM Plex Sans", 14,)  # Set font family
        self.sign_in_button = tk.Button(self.left_container, text="Sign In", font=button_font, command=self.controller.sign_in, bd=0, relief="flat", height=2)  # Remove outline and increase height
        self.sign_in_button.grid(row=4, column=0, pady=(20, 10), padx=10, sticky="ew")  # Add padding

        # Label "or" below the sign-in button
        or_label = tk.Label(self.left_container, text="or", font=button_font, bg="#BFBFBF", fg=label_fg)
        or_label.grid(row=5, column=0, pady=(10, 5))

        # Sign-up button with black background and white text
        self.sign_up_button = tk.Button(self.left_container, text="Sign Up", font=button_font, command=self.controller.open_sign_up_page, bg="black", fg="black",  bd=0, relief="flat", height=2)  # Remove outline and increase height
        self.sign_up_button.grid(row=6, column=0, pady=(5, 10), padx=10, sticky="ew")  # Add padding

        # View Attendance button
        self.view_attendance_button = tk.Button(self.left_container, text="View Attendance", font=("IBM Plex Sans", 14), command=self.view_attendance)
        self.view_attendance_button.grid(row=7, column=0, pady=(5, 10), padx=10, sticky="ew")  # Add padding

        # Right container with ATTENDANCE MANAGEMENT SYSTEM label
        self.right_container = tk.Frame(self, bg="#342E37")  # Set background color to 342E37
        self.right_container.pack(side="right", fill="both", expand=True)

        # Right container widgets
        title_font = ("IBM Plex Sans", 25, "bold")  # Set font family to IBM Plex Sans and bold
        self.title_label = tk.Label(self.right_container, text="ATTENDANCE \n MANAGEMENT SYSTEM", fg="white", bg="#342E37", font=title_font)  # Set background color to 342E37
        self.title_label.pack(expand=True, anchor="center")

    def view_attendance(self):
        password = simpledialog.askstring("Password", "Enter Password:", show="*")
        if password == "admin":
            print("Logged in successfully")
            self.open_folder()

        else:
            print("Incorrect password")

    def open_folder(self):
        folder_path = "./attendanceList"
        if os.path.exists(folder_path):
            subprocess.Popen(["open", folder_path])  # Opens the folder in Finder on macOS
        else:
            print("Attendance List folder does not exist.")
