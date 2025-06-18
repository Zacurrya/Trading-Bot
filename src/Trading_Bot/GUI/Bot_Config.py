import customtkinter as ctk
import threading 
from Trading_Bot.Logic import bot
import logging
import customtkinter as ctk

# Set up logging
logger = logging.getLogger("Log")
logging.basicConfig(filename='src/Trading_Bot/bot.log', level=logging.INFO)

class Bot_Config():

    def __init__(self, root, main_frame, log):
        # Create a frame for the bot configuration
        self.bot_config_frame = ctk.CTkFrame(main_frame, fg_color=main_frame.cget("fg_color"))
        
        # Options
        self.pairs = ["GBP_JPY", "GBP_EUR", "GBP_USD"]
        self.periods = ["M1", "M5", "M15", "M30", "H1", "H4", "D", "W"]

        # Instrument selection
        self.pairsSelect = ctk.CTkComboBox(
            self.bot_config_frame, 
            values=self.pairs, 
            width=180, height=40,
            fg_color="#0D202B",
            border_color="#0D202B",
            corner_radius=25,
            dropdown_fg_color="#0D202B",
            dropdown_hover_color="#102D3D",
            dropdown_font=("Inter", 20),
            button_color="#0D202B",
            font=("Inter", 24), 
            justify="left",
            state="readonly"
            )
        self.pairsSelect.set("GBP_JPY") # Default selection

        # Timeframe selection
        self.timeSelect = ctk.CTkComboBox(
            self.bot_config_frame, 
            values=self.periods, 
            width=120, height=40,
            fg_color="#0D202B",
            border_color="#0D202B",
            corner_radius=25,
            dropdown_fg_color="#0D202B",
            dropdown_hover_color="#102D3D",
            dropdown_font=("Inter", 20),
            button_color="#0D202B",
            font=("Inter", 24), 
            justify="center",
            state="readonly"
            )
        self.timeSelect.set("M15") # Default selection

        # Variables for bot control
        self.running = False # Initial state of the bot
        self.bot_thread = None # To hold the bot's thread
        self.stop_event = threading.Event() # Event to signal the bot to stop

        def toggle_bot():
            if not self.running: 
                # Start bot
                self.running = True
                self.toggleBotBtn.configure(text="Stop Bot", fg_color="#CC6060") 
                self.stop_event.clear()  # Ensure the stop event is cleared before starting the bot

                # Start a new thread for the bot's operation
                # Pass the stop_event, timeframe, and instrument to the bot's run function
                self.bot_thread = threading.Thread(
                    target=bot.run_bot, 
                    args=(self.stop_event, self.timeSelect.get(), self.pairsSelect.get(), log)
                )
                self.bot_thread.daemon = True  # Ensure the thread will exit when the main program does
                self.bot_thread.start()  # Start the bot thread

            else:
                # Stop bot
                self.toggleBotBtn.configure(text="Start Bot", fg_color="#60CC60")  
                bot.stop_bot(self, log)

        # Handles window closing, ensuring the bot stops before exiting
        def on_closing(): 
            if self.running:
                self.stop_event.set()
                if self.bot_thread and self.bot_thread.is_alive():
                    self.bot_thread.join(timeout=0.5)
            root.destroy()

        # Toggle button to start/stop the bot
        self.toggleBotBtn = ctk.CTkButton(self.bot_config_frame)
        self.toggleBotBtn.configure(
            text="Start Bot", 
            command=toggle_bot, 
            corner_radius=25,
            width=12, height=2, fg_color="#48B948", text_color="white",
            font=("Inter", 35, "bold")
        )

        # Position elements
        self.timeSelect.grid(row=1, column=1, padx=0)
        self.pairsSelect.grid(row=1, column=0, padx=0)
        self.toggleBotBtn.grid(row=2, column=0, padx=0, pady=20)

        # Ensures the bot stops when the window is closed
        root.protocol("WM_DELETE_WINDOW", on_closing)
