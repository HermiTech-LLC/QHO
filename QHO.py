import wx
import wx.html2
import numpy as np
import logging
from scipy.constants import hbar, pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import threading
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_QUANTUM_NUMBER = 1
DEFAULT_TIME_VALUE = 0
SLIDER_SCALE_FACTOR = 50
X_RANGE = (-10, 10)
X_POINTS = 5000
OMEGA = 1.0
MASS = 1.0

class QuantumHarmonicOscillatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.selected_n = DEFAULT_QUANTUM_NUMBER
        self.time_value = DEFAULT_TIME_VALUE
        self.init_ui()

    def init_ui(self):
        self.panel = wx.Panel(self)

        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.on_slider_scroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        # Matplotlib figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.comboBox, 1, wx.EXPAND | wx.ALL, 5)
        topSizer.Add(self.speedSlider, 2, wx.EXPAND | wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(self.infoText, 0, wx.ALL, 5)

        self.panel.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

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

        self.axes.clear()
        self.axes.plot(x, real_part, label='Real Part', linewidth=2)
        self.axes.plot(x, imag_part, label='Imaginary Part', linewidth=2)
        self.axes.plot(x, prob_density, label='Probability Density', linewidth=2, linestyle='dashed')
        self.axes.set_xlabel('Position')
        self.axes.set_ylabel('Value')
        self.axes.set_title("Quantum Harmonic Oscillator")
        self.axes.legend()
        self.canvas.draw()

        self.infoText.SetLabel(f"Quantum number n={self.selected_n}\nTime: {self.time_value:.2f}")

    def psi_n(self, x, n=0):
        coeff = (MASS * OMEGA / (pi * hbar)) ** 0.25
        hermite_n = np.polynomial.hermite.hermval(np.sqrt(MASS * OMEGA / hbar) * x, [0] * n + [1])
        normalization = np.sqrt(2 ** n * math.factorial(n))
        return coeff / normalization * hermite_n * np.exp(-MASS * OMEGA * x ** 2 / (2 * hbar))

    def time_dependent(self, n, t):
        return np.exp(-1j * (n + 0.5) * OMEGA * t)

    def psi(self, x, t, n=0):
        return self.psi_n(x, n) * self.time_dependent(n, t)

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
    app.MainLoop()