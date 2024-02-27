import wx
import wx.html2
import numpy as np
import threading
import logging
import math
from scipy.constants import hbar, pi
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO)

class QuantumHarmonicOscillatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.selected_n = 0
        self.time_value = 0
        self.init_ui()
        self.init_dash_app()
        self.start_time_update()

    def init_ui(self):
        self.panel = wx.Panel(self)
        self.init_widgets()
        self.layout_widgets()

    def init_widgets(self):
        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.on_slider_scroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        self.browser = wx.html2.WebView.New(self.panel)

    def layout_widgets(self):
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.comboBox, 1, wx.EXPAND | wx.ALL, 5)
        topSizer.Add(self.speedSlider, 2, wx.EXPAND | wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(self.browser, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.infoText, 0, wx.ALL, 5)

        self.panel.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

    def init_dash_app(self):
        self.dash_app = dash.Dash(__name__)
        self.dash_app.layout = html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(id='graph-update', interval=1000)  # Update every 1 second for animation
        ])
        self.dash_app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])(self.update_graph_scatter)

    def start_time_update(self):
        threading.Thread(target=self.update_time, daemon=True).start()

    def update_time(self):
        while True:
            self.time_value += 0.05
            time.sleep(0.1)  # Update time every 0.1 seconds for smoother animation
            wx.CallAfter(self.update_graph)

    def on_select(self, event):
        self.selected_n = int(event.GetString())
        wx.CallAfter(self.update_graph)  # Update graph immediately on user input

    def on_slider_scroll(self, event):
        self.time_value = self.speedSlider.GetValue() / 50
        wx.CallAfter(self.update_graph)  # Update graph immediately on user input

    def update_graph(self):
        try:
            x = np.linspace(-5, 5, 1000)
            psi = self.psi(x, self.time_value, n=self.selected_n)
            psi_line = go.Scatter(x=x, y=np.abs(psi) ** 2, mode='lines', name='Probability Density')
            real_line = go.Scatter(x=x, y=np.real(psi), mode='lines', name='Real Part')
            imag_line = go.Scatter(x=x, y=np.imag(psi), mode='lines', name='Imaginary Part')
            fig = go.Figure(data=[psi_line, real_line, imag_line])
            return fig
        except Exception as e:
            logging.error(f"Error updating graph: {e}")
            return go.Figure()

    def update_graph_scatter(self, n):
        return self.update_graph()

    @staticmethod
    def psi_n(x, n=0):
        m = 1.0
        omega = 1.0
        coeff = (m * omega / (pi * hbar)) ** 0.25
        hermite_n = np.polynomial.hermite.hermval(np.sqrt(m * omega / hbar) * x, [0] * n + [1])
        return coeff / np.sqrt(2 ** n * math.factorial(n)) * hermite_n * np.exp(-m * omega * x ** 2 / (2 * hbar))

    @staticmethod
    def time_dependent(n, t):
        omega = 1.0
        return np.exp(-1j * (n + 0.5) * omega * t)

    def psi(self, x, t, n=0):
        return self.psi_n(x, n) * self.time_dependent(n, t)

def run_dash_app(app, frame):
    try:
        serve(app.server, host="127.0.0.1", port=8050)
    except Exception as e:
        logging.error(f"Error running Dash app: {e}")

if __name__ == '__main__':
    try:
        app = wx.App()
        frame = QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
        threading.Thread(target=run_dash_app, args=(frame.dash_app, frame), daemon=True).start()
        app.MainLoop()
    except Exception as e:
        logging.error(f"Application failed: {e}")