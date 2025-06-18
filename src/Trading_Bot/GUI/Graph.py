import tkinter as tk
import plotly.graph_objects as go
import plotly.io as pio
import io
import kaleido
from PIL import Image, ImageTk
import threading
import Trading_Bot.Logic.bot as bot

class Graph():
    def __init__(self, main_frame, instrument, granularity):
        self.df = bot.get_candles(granularity, instrument)
        self.graph_frame = tk.Frame(main_frame)
        self.graph_frame.pack(anchor=tk.NE, padx=10, pady=10)
        self.show_graph(self.df)
        self.image_label = tk.Label(self.graph_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

    def generate_and_show_graph(self, df):
        if not df.empty:
            """
            Pulls dataframe from bot.py
            Creates a candlestick chart using Plotly
            Converts the chart to an HTML file
            and returns the file path.
            """
            fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
            fig.update_layout(
                xaxis_rangeslider_visible=False
            )

        try:
            self.img_bytes = pio.to_image(fig, format='png', width=400, height=300)
            self.image == Image.open(io.BytesIO(self.img_bytes))
            self.tk_image = ImageTk.PhotoImage(self.image)
        except Exception as e:
            print(f"Error converting Plotly figure to image: {e}")
            return