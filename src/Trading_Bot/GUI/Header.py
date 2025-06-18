import customtkinter as ctk
import Trading_Bot.Logic.login as login
class Header():
    def __init__(self, main_frame):


        #   Create header frame 
        self.header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#0D202B",
            border_color="#12222B",
            border_width=1,
            height=100,
        )

        #   Create header label
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Trading Bot", 
            font=("Inter", 22), 
            text_color="#FFFFFF", 
            fg_color="#0D202B",
            corner_radius=0,
            )
        self.title_label.grid(row=0, column=0, padx=5, pady=5)

        self.login_button = ctk.CTkButton(self.header_frame, text="Login")
        self.login_button.configure(
            text="Login",
            #command=,
            corner_radius=10,
            width=100,
            height=30,
            fg_color="#48B948",
            text_color="white",
            font=("Inter", 16, "bold")
        )
