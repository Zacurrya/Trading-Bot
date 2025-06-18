import customtkinter as ctk
import time

class Log():
    def __init__(self, root, parent_frame):  
          
        self.root = root
        self.log_file = 'src/Trading_Bot/bot.log'

        # Clear previous logs
        with open(self.log_file, 'w') as f:
            f.truncate(0) # Truncate to 0 btytes to clear the file

        # LOG FRAME
        self.log_frame = ctk.CTkFrame(parent_frame)
        self.log_frame.configure(
            fg_color=parent_frame.cget("fg_color"),
            width=20,
        )

        # LOG HEADER
        self.header_frame = ctk.CTkFrame(self.log_frame, fg_color=parent_frame.cget("fg_color"))
        self.header_frame.pack()
        self.header_label = ctk.CTkLabel(self.header_frame)
        self.header_label.configure(
            text="Log",
            fg_color="#FFFFFF", 
            text_color="#000000",
            corner_radius=12,
            width=5,                     
            font=("Inter", 20, "bold")
            )
            
        self.header_label.pack(side=ctk.TOP)

        # SCROLLABLE LOG CONTAINER
        self.log_content_frame = ctk.CTkScrollableFrame(self.log_frame)
        self.log_content_frame.configure(
            fg_color="#FFFFFF",
            corner_radius=20,
            border_color="#FFFFFF",
            scrollbar_button_color="#0D202B",
        )
        self.log_content_frame.pack()
             
    def add_log(self, log_message):
        log_label = ctk.CTkLabel(self.log_content_frame, text=log_message)
        log_label.configure(
            fg_color=self.log_content_frame.cget("fg_color"),  # Background colour of the log
            font=("Inter", 18, "bold"), 
            anchor="w",
            justify="left",
            text_color=self.choose_text_colour(log_message)  # Choose text colour based on log msg
        )
        log_label.pack(padx=0, pady=0)

    def choose_text_colour(self, log):
        # Colour will depend on whether an order has been placed, an error, order closes, etc.
        if log == "Starting bot...": return "#3E8A27" 
        elif log == "Stopping bot...": return "#BD8338"
        elif log.startswith("Order"): return "#2AB648"  # Blue for info logs
        elif log.startswith("Strategy"): return "#000000"
        else: return "#000000"





        
        