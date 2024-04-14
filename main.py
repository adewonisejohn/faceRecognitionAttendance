# main.py

import tkinter as tk
from Views.signinView import SignInView
from Controllers.signinController import SignInController

if __name__ == "__main__":
   controller = SignInController()
   controller.view.mainloop()