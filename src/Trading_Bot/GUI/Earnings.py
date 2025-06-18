import customtkinter as ctk

class Earnings():

    def __init__(self, main_frame):
        self.earnings = 0.0

        self.earnings_label = ctk.CTkLabel(
            main_frame, text=f"P/L: £{self.earnings:.2f}", font=("Inter", 16, "bold"), 
            text_color="#FFFFFF", 
            fg_color="#061118"
        )
        if self.earnings >= 0:
            self.earnings_label.configure(fg="#1AE41A")
        else:
            self.earnings_label.configure(fg="#E61919")