# Quantum Harmonic Oscillator Visualization Tool
![Quantum Harmonic Oscillator Visualization](https://github.com/LoQiseaking69/QHO/blob/main/IMG_7503.PNG)

## Overview
This Python application offers a dynamic and interactive visualization of the quantum harmonic oscillator, which is a cornerstone concept in quantum mechanics. It enables users to delve into the intricate quantum states of a particle confined in a harmonic potential, providing a graphical representation of probability densities and their evolution over time.

## Features
- **Detailed Quantum State Visualization**: Graphically represent the probability density, real part, and imaginary part of the wavefunction of a quantum harmonic oscillator.
- **Interactive Quantum State Selector**: Choose and explore various quantum states (`n`) using an intuitive dropdown menu.
- **Dynamic Time Evolution Display**: Witness the time-dependent changes in quantum states with an adjustable speed slider, animating the wavefunction in real-time.
- **Immediate Real-time Feedback**: As parameters like quantum number and time are adjusted, the plot updates instantly, offering immediate visual insights.
- **Scientific Precision**: Employs accurate scientific constants and equations for realistic and educational simulations.

## System Requirements
To run this tool, you'll need:
- Python 3.x
- wxPython for GUI elements
- NumPy for numerical operations
- Dash for web-based interactivity
- Plotly for plotting graphs
- SciPy for scientific computations

## Installation
First, ensure Python 3.x is installed on your system. Then, install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

## Running the Application
Launch the application by running the Python script. This will open the GUI with the oscillator visualization:

```bash
python QHO.py
```

## Usage Guide
- **Quantum State Selection**: Use the dropdown menu to select a quantum number (`n`). The visualization will update to display the wavefunction of the chosen quantum state.
- **Animation Speed Control**: Adjust the speed of the wavefunction's time evolution using the slider.
- **Observing Wavefunction Components**: The main plot exhibits the probability density `|ÃÂ(x,t)|^2`, along with the real and imaginary components of the wavefunction, providing a comprehensive view of the quantum state.

## Contributing
Your contributions are invaluable in enhancing and expanding the capabilities of this tool. Feel free to fork the repository, make your modifications, and submit a pull request with your improvements.

## License
This project is under the [GNU Affero General Public License v3](https://github.com/LoQiseaking69/QHO/blob/main/LICENSE).

## Acknowledgments
Designed as an educational resource, this tool aims to facilitate a deeper understanding of quantum mechanics principles. Its development and usage are intended primarily for educational and research purposes.
