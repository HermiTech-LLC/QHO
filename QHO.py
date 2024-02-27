import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.animation as animation
from scipy.constants import hbar, pi

class QuantumHarmonicOscillatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super(QuantumHarmonicOscillatorFrame, self).__init__(parent, title=title, size=(800, 600))
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.panel, -1, self.fig)

        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.comboBox, 1, wx.EXPAND | wx.ALL, 5)
        topSizer.Add(self.speedSlider, 2, wx.EXPAND | wx.ALL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(self.canvas, 1, wx.EXPAND)
        mainSizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        mainSizer.Add(self.infoText, 0, wx.ALL, 5)

        self.panel.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

        self.selected_n = 0
        self.animate()

    def OnSelect(self, event):
        self.selected_n = int(event.GetString())
        self.animate()

    def OnSliderScroll(self, event):
        self.animate()

    def animate(self):
        x = np.linspace(-5, 5, 1000)
        self.fig.clf()
        gs = self.fig.add_gridspec(3, 1)
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax2 = self.fig.add_subplot(gs[1, 0])
        ax3 = self.fig.add_subplot(gs[2, 0])

        psi_line, = ax1.plot([], [], lw=2, color='blue')
        real_line, = ax2.plot([], [], lw=2, color='green')
        imag_line, = ax3.plot([], [], lw=2, color='red')
        potential_line, = ax1.plot(x, 0.5 * x ** 2, color='orange')

        for ax in [ax1, ax2, ax3]:
            ax.set_xlim(-5, 5)
            ax.set_ylim(-1, 1)

        ax1.set_title("Probability Density |ψ|^2")
        ax2.set_title("Real Part of ψ")
        ax3.set_title("Imaginary Part of ψ")

        def init():
            psi_line.set_data([], [])
            real_line.set_data([], [])
            imag_line.set_data([], [])
            return psi_line, real_line, imag_line, potential_line

        def animate(i):
            psi = self.psi(x, i / 100 * self.speedSlider.GetValue(), n=self.selected_n)
            psi_line.set_data(x, np.abs(psi) ** 2)
            real_line.set_data(x, np.real(psi))
            imag_line.set_data(x, np.imag(psi))
            self.infoText.SetLabel(f"Quantum number n={self.selected_n}\nTime: {i / 10:.1f}")
            return psi_line, real_line, imag_line, potential_line

        if hasattr(self, 'ani'):
            self.ani.event_source.stop()

        self.ani = animation.FuncAnimation(self.fig, animate, init_func=init, frames=200, interval=50, blit=True)

    @staticmethod
    def psi_n(x, n=0):
        m = 1.0
        omega = 1.0
        coeff = (m * omega / (pi * hbar)) ** 0.25
        hermite_n = np.polynomial.hermite.hermval(np.sqrt(m * omega / hbar) * x, [0] * n + [1])
        return coeff / np.sqrt(2 ** n * np.math.factorial(n)) * hermite_n * np.exp(-m * omega * x ** 2 / (2 * hbar))

    @staticmethod
    def time_dependent(n, t):
        omega = 1.0
        return np.exp(-1j * (n + 0.5) * omega * t)

    def psi(self, x, t, n=0):
        return self.psi_n(x, n) * self.time_dependent(n, t)

app = wx.App()
QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
app.MainLoop()