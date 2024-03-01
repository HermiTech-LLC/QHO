import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from scipy.constants import hbar, pi
import math

# Constants
MASS = OMEGA = HBAR = 1  # You can adjust these constants if needed

# Function for the wave function
def psi_n(x, n=0):
    coeff = (MASS * OMEGA / (np.pi * HBAR)) ** 0.25
    hermite_n = np.polynomial.hermite.hermval(
        np.sqrt(MASS * OMEGA / HBAR) * x, [0] * n + [1]
    )
    normalization = np.sqrt(2 ** n * math.factorial(n))
    return coeff / normalization * hermite_n * np.exp(-MASS * OMEGA * x ** 2 / (2 * HBAR))

# Function for time-dependent part
def time_dependent(n, t):
    return np.exp(-1j * (n + 0.5) * OMEGA * t)

# Function for the total wave function
def psi(x, t, n=0):
    return psi_n(x, n) * time_dependent(n, t)

# Function for probability density
def probability_density(x, t, n=0):
    return np.abs(psi(x, t, n))**2

# Quantum Harmonic Oscillator Frame Class
class QuantumHarmonicOscillatorFrame(wx.Frame):
    DEFAULT_QUANTUM_NUMBER = 0  # Ground state
    TIME_SLIDER_SCALE = 100
    X_RANGE = (-2, 2)
    X_POINTS = 2000

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.selected_n = self.DEFAULT_QUANTUM_NUMBER
        self.time_value = 0
        self.init_ui()

    def init_ui(self):
        self.panel = wx.Panel(self)
        self.setup_controls()
        self.setup_layout()
        self.Centre()
        self.Show(True)
        self.update_graph()

    def setup_controls(self):
        self.comboBox = wx.ComboBox(
            self.panel, choices=[str(i) for i in range(5)], style=wx.CB_READONLY
        )
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.on_select)
        self.comboBox.SetSelection(self.DEFAULT_QUANTUM_NUMBER)

        self.timeSlider = wx.Slider(
            self.panel, value=0, minValue=0, maxValue=self.TIME_SLIDER_SCALE,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.timeSlider.Bind(wx.EVT_SLIDER, self.on_slider_scroll)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.axes = self.figure.add_subplot(111)

        self.insightsPanel = wx.TextCtrl(
            self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP
        )
        self.insightsPanel.SetBackgroundColour(wx.Colour(255, 255, 255))

    def setup_layout(self):
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        controlSizer.Add(self.comboBox, 1, wx.EXPAND | wx.ALL, 5)
        controlSizer.Add(self.timeSlider, 2, wx.EXPAND | wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(controlSizer, 0, wx.EXPAND)
        mainSizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(mainSizer)

    def on_select(self, event):
        self.selected_n = int(event.GetString())
        self.update_graph()

    def on_slider_scroll(self, event):
        self.time_value = event.GetInt() / self.TIME_SLIDER_SCALE
        self.update_graph()

    def update_graph(self):
        x = np.linspace(*self.X_RANGE, self.X_POINTS)
        wave_function = psi(x, self.time_value, n=self.selected_n)
        real_part = np.real(wave_function)
        imaginary_part = np.imag(wave_function)
        prob_density = np.abs(wave_function) ** 2

        self.axes.clear()
        self.axes.plot(x, real_part, label='Real Part', linewidth=2)
        self.axes.plot(x, imaginary_part, label='Imaginary Part', linewidth=2)
        self.axes.plot(x, prob_density, label='Probability Density', linewidth=2, linestyle='dashed')

        # Include the wave function's mathematical expression
        expression = (r'$\Psi(x,t) = \left(\frac{m\omega}{\pi \hbar}\right)^{1/4} \times$'
                      r'$H_n(\sqrt{\frac{m\omega}{\hbar}}x) \times$'
                      r'$e^{-\frac{m\omega x^2}{2\hbar}} \times e^{-i\omega t(n+\frac{1}{2})}$')
        self.axes.text(0.05, 0.95, expression, fontsize=10, color='blue', transform=self.axes.transAxes,
                       verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

        self.axes.set_xlabel('Position (x)')
        self.axes.set_ylabel('Wave Function / Probability Density')
        self.axes.set_title('Quantum Harmonic Oscillator')
        self.axes.legend()
        self.canvas.draw()

        # Update insights panel with the wave function's expression
        self.insightsPanel.SetValue(f"Wave function for n={self.selected_n}, t={self.time_value:.2f}:\n" + expression)

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
    app.MainLoop()
