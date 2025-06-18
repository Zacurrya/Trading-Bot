import customtkinter as ctk

class Timer():
    def __init__(self, root):

        self.run_time = '00:00:00'

        # Timer label
        self.timer_label = ctk.CTkLabel(root, text=self.run_time)
