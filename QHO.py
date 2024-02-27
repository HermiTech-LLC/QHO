import wx
import wx.html2
import numpy as np
import logging
import math
from scipy.constants import hbar, pi
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input
from waitress import serve
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_QUANTUM_NUMBER = 1
DEFAULT_TIME_VALUE = 0
SLIDER_SCALE_FACTOR = 50
X_RANGE = (-5, 5)
X_POINTS = 1000
OMEGA = 1.0  # Angular frequency
MASS = 1.0   # Mass
DASH_HOST = '127.0.0.1'
DASH_PORT = 8050

class QuantumHarmonicOscillatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.selected_n = DEFAULT_QUANTUM_NUMBER
        self.time_value = DEFAULT_TIME_VALUE
        self.init_ui()
        self.init_dash_app()
        threading.Thread(target=self.run_dash_app, daemon=True).start()

    def init_ui(self):
        self.panel = wx.Panel(self)
        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.on_slider_scroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        self.browser = wx.html2.WebView.New(self.panel)
        self.browser.LoadURL(f'http://{DASH_HOST}:{DASH_PORT}')

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
            dcc.Graph(id='live-graph', animate=False),
            dcc.Interval(id='graph-update', interval=1000 * 1000, disabled=True)
        ])
        self.dash_app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])(self.update_graph)

    def on_select(self, event):
        self.selected_n = int(event.GetString())
        self.update_graph()

    def on_slider_scroll(self, event):
        self.time_value = self.speedSlider.GetValue() / SLIDER_SCALE_FACTOR
        self.update_graph()

    def update_graph(self, n_intervals=None):
        x = np.linspace(*X_RANGE, X_POINTS)
        psi = self.psi(x, self.time_value, n=self.selected_n)
        prob_density = np.abs(psi) ** 2
        real_part = np.real(psi)
        imag_part = np.imag(psi)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=prob_density, mode='lines', name='Probability Density'))
        fig.add_trace(go.Scatter(x=x, y=real_part, mode='lines', name='Real Part'))
        fig.add_trace(go.Scatter(x=x, y=imag_part, mode='lines', name='Imaginary Part'))

        fig.update_layout(
            title="Quantum Harmonic Oscillator",
            xaxis_title="Position",
            yaxis_title="Value",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        self.infoText.SetLabel(f"Quantum number n={self.selected_n}\nTime: {self.time_value:.2f}")
        self.browser.Reload()  # This line will refresh the WebView to display the updated graph
        return fig

    def psi_n(self, x, n=0):
        coeff = (MASS * OMEGA / (pi * hbar)) ** 0.25
        hermite_n = np.polynomial.hermite.hermval(np.sqrt(MASS * OMEGA / hbar) * x, [0] * n + [1])
        normalization = np.sqrt(2 ** n * math.factorial(n))
        return coeff / normalization * hermite_n * np.exp(-MASS * OMEGA * x ** 2 / (2 * hbar))

    def time_dependent(self, n, t):
        return np.exp(-1j * (n + 0.5) * OMEGA * t)

    def psi(self, x, t, n=0):
        return self.psi_n(x, n) * self.time_dependent(n, t)

    def run_dash_app(self):
        serve(self.dash_app.server, host=DASH_HOST, port=DASH_PORT)

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
    app.MainLoop()