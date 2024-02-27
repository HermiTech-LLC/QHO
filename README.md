# Quantum Harmonic Oscillator Visualization Tool
![img](https://github.com/LoQiseaking69/QHO/blob/main/IMG_7503.PNG)

## Overview
This Python application provides an interactive visualization of the quantum harmonic oscillator, a fundamental concept in quantum mechanics. It allows users to explore the quantum states of a particle in a harmonic potential, visualizing the probability densities and their time evolution.

## Features
- **Quantum State Visualization**: Plot the probability density, real part, and imaginary part of the quantum harmonic oscillator's wavefunction.
- **Interactive Quantum State Selection**: Choose from different quantum states (`n`) using a dropdown menu.
- **Dynamic Time Evolution**: Observe how the quantum state evolves over time with an adjustable animation speed slider.
- **Real-time Updates**: The plot updates in real time as parameters are changed, providing immediate visual feedback.
- **Scientific Accuracy**: Utilizes proper scientific constants and equations for realistic simulations.

## Requirements
- Python 3.x
- wxPython
- NumPy
- Dash
- Plotly
- SciPy

## Installation
Ensure you have Python installed, then install the required packages using pip:
```
pip install -r requirements.txt
```

## Running the Application
To run the application, execute the Python script containing the code. The GUI should launch, displaying the visualization.

```bash
python QHO.py
```

## Usage
- **Selecting Quantum State**: Use the dropdown menu to choose a quantum number (`n`). The plot will update to show the corresponding quantum state.
- **Adjusting Animation Speed**: Use the slider to control the speed of the time evolution animation.
- **Viewing Probability Densities and Wavefunction Components**: The main plot area displays the probability density `|Ï(x,t)|^2`, real part, and imaginary part of the wavefunction.

## Contributing
Contributions to enhance or expand the functionality of this tool are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License
Found here: [GNU affero v3](https://github.com/LoQiseaking69/QHO/blob/main/LICENSE).

## Acknowledgments
This tool was created to aid in the understanding of quantum mechanics principles and is intended for educational purposes.