import wx
import wx.html2
import numpy as np
import threading
import logging
import math
import time
from scipy.constants import hbar, pi
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO)

class QuantumHarmonicOscillatorFrame(wx.Frame):
    """A frame for the Quantum Harmonic Oscillator visualization."""

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.selected_n = 0
        self.time_value = 0
        self.init_ui()
        self.init_dash_app()
        self.start_time_update()

    def init_ui(self):
        """Initialize the UI components."""
        self.panel = wx.Panel(self)
        self.init_widgets()
        self.layout_widgets()

    def init_widgets(self):
        """Create and bind UI widgets."""
        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.on_slider_scroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        self.browser = wx.html2.WebView.New(self.panel)

    def layout_widgets(self):
        """Layout the UI widgets."""
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
        """Initialize the Dash app for plotting."""
        self.dash_app = dash.Dash(__name__)
        self.dash_app.layout = html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(id='graph-update', interval=60000)  # Update every 60 seconds
        ])
        self.dash_app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])(self.update_graph_scatter)
        self.update_graph()  # Render initial graph

    def start_time_update(self):
        """Start the thread for time updates."""
        threading.Thread(target=self.update_time, daemon=True).start()

    def update_time(self):
        """Update the time and refresh the graph."""
        while True:
            self.time_value += 0.05
            time.sleep(60)  # Wait for 60 seconds
            wx.CallAfter(self.update_graph)

    def on_select(self, event):
        """Handle selection of quantum number."""
        self.selected_n = int(event.GetString())
        self.update_graph()

    def on_slider_scroll(self, event):
        """Handle slider scroll event."""
        self.time_value = self.speedSlider.GetValue() / 50
        self.update_graph()

    def update_graph(self):
        """Update the graph with the latest data."""
        x = np.linspace(-5, 5, 1000)
        psi = self.psi(x, self.time_value, n=self.selected_n)
        psi_line = go.Scatter(x=x, y=np.abs(psi) ** 2, mode='lines', name='Probability Density')
        real_line = go.Scatter(x=x, y=np.real(psi), mode='lines', name='Real Part')
        imag_line = go.Scatter(x=x, y=np.imag(psi), mode='lines', name='Imaginary Part')
        fig = go.Figure(data=[psi_line, real_line, imag_line])
        self.browser.LoadURL("http://127.0.0.1:8050/")  # Ensure the browser reloads the URL
        return fig

    def update_graph_scatter(self, n):
        """Callback for Dash to update the graph."""
        return self.update_graph()

    @staticmethod
    def psi_n(x, n=0):
        """Calculate the wave function psi_n."""
        m = 1.0
        omega = 1.0
        coeff = (m * omega / (pi * hbar)) ** 0.25
        hermite_n = np.polynomial.hermite.hermval(np.sqrt(m * omega / hbar) * x, [0] * n + [1])
        return coeff / np.sqrt(2 ** n * math.factorial(n)) * hermite_n * np.exp(-m * omega * x ** 2 / (2 * hbar))

    @staticmethod
    def time_dependent(n, t):
        """Return the time-dependent factor of the wave function."""
        omega = 1.0
        return np.exp(-1j * (n + 0.5) * omega * t)

    def psi(self, x, t, n=0):
        """Calculate the complete wave function psi."""
        return self.psi_n(x, n) * self.time_dependent(n, t)

def run_dash_app(app, frame):
    """Run the Dash app in a separate thread."""
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
