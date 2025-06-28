import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from swingby.visualization.plots import OrbitPlotter


class TestOrbitPlotter:
    def test_plotter_initialization(self):
        """Test that OrbitPlotter can be initialized."""
        plotter = OrbitPlotter()
        assert plotter is not None
        assert plotter.figure_size == (6, 6)

    def test_plotter_custom_figure_size(self):
        """Test plotter initialization with custom figure size."""
        custom_size = (8, 10)
        plotter = OrbitPlotter(figure_size=custom_size)
        assert plotter.figure_size == custom_size

    def test_plot_orbit_basic(self):
        """Test basic orbit plotting functionality."""
        plotter = OrbitPlotter()

        # Create dummy data
        solutions = [np.random.rand(100, 4) * 1e8]  # Random trajectory
        planet_coordinates = {
            "earth": {"x": np.linspace(0, 1e8, 10), "y": np.linspace(0, 1e8, 10)}
        }

        # Should not raise an exception
        plotter.plot_orbit(solutions, planet_coordinates)

    def test_plot_distance_basic(self):
        """Test basic distance plotting functionality."""
        plotter = OrbitPlotter()

        # Create dummy data
        timeseries = pd.date_range(datetime(2022, 1, 1), periods=100, freq="D")
        distance = np.random.rand(100) * 1e8

        # Should not raise an exception
        plotter.plot_distance(timeseries, distance)



