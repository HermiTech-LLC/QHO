import wx
import wx.html2
import numpy as np
from scipy.constants import hbar, pi
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input

class QuantumHarmonicOscillatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super(QuantumHarmonicOscillatorFrame, self).__init__(parent, title=title, size=(800, 600))
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)

        self.comboBox = wx.ComboBox(self.panel, choices=[str(i) for i in range(10)], style=wx.CB_READONLY)
        self.comboBox.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.comboBox.SetSelection(0)

        self.speedSlider = wx.Slider(self.panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.speedSlider.Bind(wx.EVT_SLIDER, self.OnSliderScroll)

        self.infoText = wx.StaticText(self.panel, label="Quantum number n=0\nTime: 0.0")

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(self.comboBox, 1, wx.EXPAND | wx.ALL, 5)
        topSizer.Add(self.speedSlider, 2, wx.EXPAND | wx.ALL, 5)

        # Dash Application
        self.dash_app = dash.Dash(__name__)
        self.dash_app.layout = html.Div([
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(id='graph-update', interval=1000)
        ])

        # Embedding Dash in wxPython
        self.browser = wx.html2.WebView.New(self.panel)
        self.server = self.dash_app.server
        self.browser.LoadURL("http://127.0.0.1:8050/")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(self.browser, 1, wx.EXPAND)
        mainSizer.Add(self.infoText, 0, wx.ALL, 5)

        self.panel.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

        self.selected_n = 0
        self.speed_value = 50

    def OnSelect(self, event):
        self.selected_n = int(event.GetString())
        self.dash_app.callback_context.response.set_data(self.update_graph())

    def OnSliderScroll(self, event):
        self.speed_value = self.speedSlider.GetValue()
        self.dash_app.callback_context.response.set_data(self.update_graph())

    def update_graph(self):
        x = np.linspace(-5, 5, 1000)
        psi = self.psi(x, self.speed_value, n=self.selected_n)
        psi_line = go.Scatter(x=x, y=np.abs(psi) ** 2, mode='lines', name='Probability Density')
        real_line = go.Scatter(x=x, y=np.real(psi), mode='lines', name='Real Part')
        imag_line = go.Scatter(x=x, y=np.imag(psi), mode='lines', name='Imaginary Part')
        fig = go.Figure(data=[psi_line, real_line, imag_line])
        return fig

    # Callback for updating the graph
    @self.dash_app.callback(Output('live-graph', 'figure'),
                            [Input('graph-update', 'n_intervals')])
    def update_graph_scatter(n):
        return self.update_graph()

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

if __name__ == '__main__':
    app = wx.App()
    frame = QuantumHarmonicOscillatorFrame(None, title='Quantum Harmonic Oscillator Visualization')
    frame.dash_app.run_server()
    app.MainLoop()