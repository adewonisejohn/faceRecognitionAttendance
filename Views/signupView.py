import tkinter as tk
class SignUpView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Sign Up")
        self.geometry("1000x600")  # Set window size

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.matric_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.level_var = tk.StringVar()

        # Left container with a deeper background color
        self.left_container = tk.Frame(self, bg="#BFBFBF")  # Set background color to a deeper shade
        self.left_container.pack(side="left", fill="both", expand=False, padx=10, pady=10)  # Add padding

        # Left container widgets
        entry_font = ("IBM Plex Sans", 30)  # Set font family to IBM Plex Sans
        entry_bg = "white"  # Set background color to a deeper shade
        entry_fg = "black"  # Set entry text color to black
        label_fg = "#666666"  # Set label text color to grey
        label_font = ("IBM Plex Sans", 15, "bold")  # Set label font to bold

        self.first_name_label = tk.Label(self.left_container, text="First Name:", fg=label_fg, bg="#BFBFBF",
                                         font=label_font)  # Set background color to a deeper shade
        self.first_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))  # Align top-left and add padding

        self.first_name_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg,
                                         font=entry_font, textvariable=self.first_name_var)  # Bind textvariable
        self.first_name_entry.grid(row=1, column=0, sticky="ew", padx=10,
                                   pady=(0, 5))  # Expand to fill horizontally, add padding

        self.last_name_label = tk.Label(self.left_container, text="Last Name:", fg=label_fg, bg="#BFBFBF",
                                        font=label_font)  # Set background color to a deeper shade
        self.last_name_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 5))  # Align top-left and add padding

        self.last_name_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg,
                                        font=entry_font, textvariable=self.last_name_var)  # Bind textvariable
        self.last_name_entry.grid(row=3, column=0, sticky="ew", padx=10,
                                  pady=(0, 5))  # Expand to fill horizontally, add padding

        self.matric_label = tk.Label(self.left_container, text="Matric Number:", fg=label_fg, bg="#BFBFBF",
                                         font=label_font)
        self.matric_label.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 5))
        self.matric_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg, font=entry_font,
                                         textvariable=self.matric_var)  # Bind textvariable
        self.matric_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.department_label = tk.Label(self.left_container, text="Department:", fg=label_fg, bg="#BFBFBF",
                                      font=label_font)
        self.department_label.grid(row=6, column=0, sticky="w", padx=10, pady=(10, 5))
        self.department_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg, font=entry_font,
                                         textvariable=self.department_var)  # Bind textvariable
        self.department_entry.grid(row=7, column=0, sticky="ew", padx=10, pady=(0, 5))

        self.level_label = tk.Label(self.left_container, text="Level:", fg=label_fg, bg="#BFBFBF",
                                     font=label_font)
        self.level_label.grid(row=8, column=0, sticky="w", padx=10, pady=(10, 5))

        self.level_entry = tk.Entry(self.left_container, bg=entry_bg, fg=entry_fg, font=entry_font,
                                    textvariable=self.level_var)  # Bind textvariable
        self.level_entry.grid(row=9, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Continue Button
        self.continue_button = tk.Button(self.left_container, text="Continue", font=entry_font,
                                         command=self.sign_up, bg="black", fg="white", bd=0, relief="flat",
                                         height=2)
        self.continue_button.grid(row=10, column=0, pady=20, padx=10, sticky="ew")

        # Right container with ATTENDANCE MANAGEMENT SYSTEM label
        self.right_container = tk.Frame(self, bg="#342E37")  # Set background color to 342E37
        self.right_container.pack(side="right", fill="both", expand=True)

        # Initialize the camera label
        self.camera_label = tk.Label(self.right_container)
        self.camera_label.pack()

        # Right container widgets
        title_font = ("IBM Plex Sans", 25, "bold")  # Set font family to IBM Plex Sans and bold
        self.title_label = tk.Label(self.right_container, text="ATTENDANCE \n MANAGEMENT SYSTEM", fg="white",
                                    bg="#342E37", font=title_font)  # Set background color to 342E37
        self.title_label.pack(expand=True, anchor="center")

    def sign_up(self):
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        matric_number = self.matric_var.get()
        phone_number = self.phone_var.get()
        department = self.department_var.get()
        level = self.level_var.get()

        self.controller.sign_up(first_name, last_name, matric_number, phone_number, department, level)