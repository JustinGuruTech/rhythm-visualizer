# Rhythm Visualizer

This Python project is a rhythm visualizer that leverages the power of `pygame` to display complex rhythmic patterns. The visualizer creates an interactive experience that displays various beat patterns, especially accentuating odd time rhythms with visually distinguishable circles.

## Installation

To run this rhythm visualizer, you will need to have Python installed on your system as well as the `pygame` library.

1. If you have not already installed Python, download and install it from [python.org](https://www.python.org/downloads/).

2. Install `pygame` using pip. Run the following command in your terminal:

    ```
    pip install pygame
    ```

## Quick Start

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Run the visualizer script:

    ```
    python viz.py
    ```

## Usage

When you run the script, a window will open displaying a number of circles representing beats in a measure. The visualizer allows you to see the rhythm of a pre-defined beat pattern configuration. You can interact with the visualizer by clicking on buttons to change the beat pattern to predefined configurations, such as 4/4 or 7/4 rhythms.

## Features

- Visualization of complex rhythmic patterns in real-time.
- Support for odd time signatures with customizable beat strength mapping.
- Interactive buttons to switch between different rhythm configurations.
- Smooth transitions between beats using a configurable smoothing factor.

## Customization

To customize the beat patterns beyond the pre-defined configurations, modify the `BeatPatternConfig` instantiation in the source code. You can adjust the `beats_per_minute`, `beats_per_measure`, and `beat_strengths` to fit the rhythm you wish to visualize.

Here is an example of a custom beat pattern:

```python
custom_pattern_config = BeatPatternConfig(
    beats_per_minute=120,
    beats_per_measure=5,
    beat_strengths=[5, 2, 1, 5, 1, 5, 2, 1, 5, 1],
)