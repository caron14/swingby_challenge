"""
Visualization and plotting functionality for orbital mechanics simulation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class OrbitPlotter:
    """
    Handles all plotting and visualization for orbital mechanics simulations.
    """

    def __init__(self, figure_size: tuple = (6, 6)):
        """
        Initialize the plotter.

        Args:
            figure_size: Default figure size as (width, height)
        """
        self.figure_size = figure_size

    def plot_orbit(
        self,
        solutions: List[np.ndarray],
        planet_coordinates: Dict,
        save_path: Optional[Union[str, Path]] = None,
        show_plot: bool = False,
    ) -> None:
        """
        Plot spacecraft orbit with planetary trajectories.

        Args:
            solutions: List of solution arrays from orbital integration
            planet_coordinates: Dictionary of planet coordinate time series
            save_path: Path to save the plot (optional)
            show_plot: Whether to display the plot interactively
        """
        fig = plt.figure(figsize=self.figure_size)

        # Plot Sun at origin
        plt.scatter(0, 0, color="orange", s=200, label="Sun")

        # Plot planetary trajectories
        for planet_name, coords in planet_coordinates.items():
            x_coords = coords["x"]
            y_coords = coords["y"]

            # Plot trajectory
            plt.plot(x_coords, y_coords, label=planet_name, linewidth=2)
            # Plot final position
            plt.scatter(x_coords[-1], y_coords[-1], s=40)

        # Plot spacecraft trajectory
        for solution in solutions:
            plt.plot(solution[:, 0], solution[:, 1], color="black", linewidth=1.5)

        # Plot final spacecraft position
        if solutions:
            final_pos = solutions[-1][-1, :2]
            plt.scatter(
                final_pos[0],
                final_pos[1],
                color="black",
                label="spacecraft",
                s=60,
                marker="s",
            )

        # Formatting
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(0.75, 0.9))
        plt.gca().set_aspect("equal")
        plt.xlabel("x (km)")
        plt.ylabel("y (km)")
        plt.title("Spacecraft Orbital Trajectory")

        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        if show_plot:
            plt.show()
        else:
            plt.close(fig)

    def plot_distance(
        self,
        timeseries: pd.DatetimeIndex,
        distance: np.ndarray,
        save_path: Optional[Union[str, Path]] = None,
        show_plot: bool = False,
    ) -> None:
        """
        Plot distance between spacecraft and Earth over time.

        Args:
            timeseries: Time series data
            distance: Distance values in km
            save_path: Path to save the plot (optional)
            show_plot: Whether to display the plot interactively
        """
        fig = plt.figure(figsize=self.figure_size)

        plt.plot(timeseries, distance, color="black", linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("Date")
        plt.ylabel("Distance (km)")
        plt.title("Spacecraft-Earth Distance")
        plt.xticks(rotation=45)

        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        if show_plot:
            plt.show()
        else:
            plt.close(fig)







