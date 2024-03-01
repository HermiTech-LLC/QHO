# Quantum Harmonic Oscillator Visualization Tool
![Quantum Harmonic Oscillator Visualization](https://github.com/LoQiseaking69/QHO/blob/main/IMG_7503.PNG)

## Overview
This Python application provides a dynamic and interactive visualization of the quantum harmonic oscillator, a fundamental concept in quantum mechanics. It enables users to explore the quantum states of a particle in a harmonic potential through graphical representations of wavefunctions and probability densities.

## Features
- **Wavefunction Visualization**: Graphical representation of the probability density, real part, and imaginary part of the quantum harmonic oscillator's wavefunction.
- **Interactive Quantum State Selector**: An intuitive dropdown menu for selecting and exploring different quantum states (`n`).
- **Dynamic Time Evolution**: Adjustable speed slider to view the time-dependent changes in quantum states, animating the wavefunction in real-time.
- **Real-time Feedback**: Instantaneous updates in the plot as parameters like quantum number and time are adjusted.
- **Scientific Accuracy**: Utilizes accurate scientific constants and equations for realistic simulations.

## System Requirements
To run this tool, you'll need:
- Python 3.x
- wxPython for GUI elements
- NumPy for numerical operations
- Matplotlib for plotting
- SciPy for scientific computations

## Installation
Ensure Python 3.x is installed on your system. Then, install the necessary Python packages:

```bash
pip install wxpython numpy matplotlib scipy
```

## Running the Application
Run the Python script to launch the application, which will open a GUI displaying the oscillator visualization:

```bash
python QHO.py
```

## Usage Guide
- **Quantum State Selection**: Select a quantum number (`n`) from the dropdown menu. The visualization updates to show the corresponding wavefunction.
- **Control Time Evolution**: Use the slider to adjust the speed of the wavefunction's time evolution.
- **Wavefunction Analysis**: The plot displays the probability density `|Ï(x,t)|Â²`, real, and imaginary components of the wavefunction for comprehensive quantum state analysis.

## Contributing
Contributions are welcome to enhance and expand the tool's capabilities. Feel free to fork the repository, make modifications, and submit pull requests with improvements.

## License
This project is under the [GNU Affero General Public License v3](https://github.com/LoQiseaking69/QHO/blob/main/LICENSE).

## Acknowledgments
This tool is designed as an educational resource to aid in understanding quantum mechanics. It's intended for educational and research purposes.
