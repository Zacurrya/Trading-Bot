import customtkinter as ctk
from PIL import Image, ImageTk  # Import ImageTk
from Trading_Bot.GUI.Header import Header
from Trading_Bot.GUI.Bot_Config import Bot_Config
from Trading_Bot.GUI.Log import Log
from Trading_Bot.GUI.Earnings import Earnings
from Trading_Bot.GUI.Timer import Timer
from Trading_Bot.GUI.Graph import Graph

class MainApplication(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.deactivate_automatic_dpi_awareness()

        # Window setup
        window_height = 700
        window_width = 900
        bg_colour = "#061118"
        self.title("Trading Bot")
        self.geometry(f"{window_width}x{window_height}")

        # Layout configuration
        self.left_margin = 10

        # Load image with PIL and convert to PhotoImage for iconphoto
        self.tk_image = ImageTk.PhotoImage(Image.open('images/robot.png'))
        self.iconphoto(False, self.tk_image)

        # Main frame
        self.main_frame = ctk.CTkFrame(self, fg_color=bg_colour)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        # Create component classes
        self.log = Log(self, self.main_frame)
        self.bot_config = Bot_Config(self, self.main_frame, self.log)
        self.header = Header(self.main_frame)
        self.earnings = Earnings(self.main_frame)
        # self.timer = Timer(self.main_frame)
        # self.graph = Graph(self.main_frame, self.bot_config.pairsSelect.get(), self.bot_config.timeSelect.get())

        # Pack components into the main frame
        self.header.header_frame.pack(side=ctk.TOP, fill=ctk.X)
        self.bot_config.bot_config_frame.pack(anchor=ctk.NW, padx=self.left_margin, pady=20)
        self.earnings.earnings_label.pack(anchor=ctk.NW, padx=5, pady=3)
        self.log.log_frame.pack(anchor=ctk.NW, padx=self.left_margin, pady=5)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
