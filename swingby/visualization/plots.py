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

    def plot_velocity_profile(
        self,
        solutions: List[np.ndarray],
        save_path: Optional[Union[str, Path]] = None,
        show_plot: bool = False,
    ) -> None:
        """
        Plot spacecraft velocity magnitude over time.

        Args:
            solutions: List of solution arrays from orbital integration
            save_path: Path to save the plot (optional)
            show_plot: Whether to display the plot interactively
        """
        fig = plt.figure(figsize=self.figure_size)

        # Calculate velocity magnitude for each solution segment
        all_velocities = []
        time_points = []
        current_time = 0

        for solution in solutions:
            velocities = np.sqrt(solution[:, 2] ** 2 + solution[:, 3] ** 2)
            all_velocities.extend(velocities)

            # Assuming daily time steps
            segment_times = np.arange(current_time, current_time + len(velocities))
            time_points.extend(segment_times)
            current_time += len(velocities)

        plt.plot(time_points, all_velocities, color="blue", linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("Time (days)")
        plt.ylabel("Velocity Magnitude (km/s)")
        plt.title("Spacecraft Velocity Profile")

        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        if show_plot:
            plt.show()
        else:
            plt.close(fig)

    def plot_energy_profile(
        self,
        solutions: List[np.ndarray],
        gm_sun: float = 1.327e11,
        save_path: Optional[Union[str, Path]] = None,
        show_plot: bool = False,
    ) -> None:
        """
        Plot spacecraft orbital energy over time.

        Args:
            solutions: List of solution arrays from orbital integration
            gm_sun: Gravitational parameter of the Sun
            save_path: Path to save the plot (optional)
            show_plot: Whether to display the plot interactively
        """
        fig = plt.figure(figsize=self.figure_size)

        all_energies = []
        time_points = []
        current_time = 0

        for solution in solutions:
            # Calculate kinetic energy
            ke = 0.5 * (solution[:, 2] ** 2 + solution[:, 3] ** 2)

            # Calculate potential energy
            r = np.sqrt(solution[:, 0] ** 2 + solution[:, 1] ** 2)
            pe = -gm_sun / r

            # Total specific energy
            total_energy = ke + pe
            all_energies.extend(total_energy)

            segment_times = np.arange(current_time, current_time + len(total_energy))
            time_points.extend(segment_times)
            current_time += len(total_energy)

        plt.plot(time_points, all_energies, color="red", linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("Time (days)")
        plt.ylabel("Specific Energy (km²/s²)")
        plt.title("Spacecraft Orbital Energy")

        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        if show_plot:
            plt.show()
        else:
            plt.close(fig)

    def create_summary_plot(
        self,
        solutions: List[np.ndarray],
        planet_coordinates: Dict,
        timeseries: pd.DatetimeIndex,
        distance: np.ndarray,
        save_path: Optional[Union[str, Path]] = None,
        show_plot: bool = False,
    ) -> None:
        """
        Create a summary plot with multiple subplots.

        Args:
            solutions: List of solution arrays from orbital integration
            planet_coordinates: Dictionary of planet coordinate time series
            timeseries: Time series data
            distance: Distance values in km
            save_path: Path to save the plot (optional)
            show_plot: Whether to display the plot interactively
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

        # Orbit plot
        plt.sca(ax1)
        self._plot_orbit_on_axis(ax1, solutions, planet_coordinates)

        # Distance plot
        plt.sca(ax2)
        self._plot_distance_on_axis(ax2, timeseries, distance)

        # Velocity plot
        plt.sca(ax3)
        self._plot_velocity_on_axis(ax3, solutions)

        # Energy plot
        plt.sca(ax4)
        self._plot_energy_on_axis(ax4, solutions)

        plt.tight_layout()

        # Save or show
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
        if show_plot:
            plt.show()
        else:
            plt.close(fig)

    def _plot_orbit_on_axis(self, ax, solutions, planet_coordinates):
        """Helper method to plot orbit on specific axis."""
        ax.scatter(0, 0, color="orange", s=100, label="Sun")

        for planet_name, coords in planet_coordinates.items():
            ax.plot(coords["x"], coords["y"], label=planet_name, linewidth=1.5)
            ax.scatter(coords["x"][-1], coords["y"][-1], s=30)

        for solution in solutions:
            ax.plot(solution[:, 0], solution[:, 1], color="black", linewidth=1)

        if solutions:
            final_pos = solutions[-1][-1, :2]
            ax.scatter(
                final_pos[0],
                final_pos[1],
                color="black",
                label="spacecraft",
                s=40,
                marker="s",
            )

        ax.grid(True, alpha=0.3)
        ax.legend(fontsize="small")
        ax.set_aspect("equal")
        ax.set_xlabel("x (km)")
        ax.set_ylabel("y (km)")
        ax.set_title("Orbit Trajectory")

    def _plot_distance_on_axis(self, ax, timeseries, distance):
        """Helper method to plot distance on specific axis."""
        ax.plot(timeseries, distance, color="black", linewidth=1.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("Date")
        ax.set_ylabel("Distance (km)")
        ax.set_title("Spacecraft-Earth Distance")
        ax.tick_params(axis="x", rotation=45)

    def _plot_velocity_on_axis(self, ax, solutions):
        """Helper method to plot velocity on specific axis."""
        all_velocities = []
        time_points = []
        current_time = 0

        for solution in solutions:
            velocities = np.sqrt(solution[:, 2] ** 2 + solution[:, 3] ** 2)
            all_velocities.extend(velocities)
            segment_times = np.arange(current_time, current_time + len(velocities))
            time_points.extend(segment_times)
            current_time += len(velocities)

        ax.plot(time_points, all_velocities, color="blue", linewidth=1.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Velocity (km/s)")
        ax.set_title("Velocity Profile")

    def _plot_energy_on_axis(self, ax, solutions, gm_sun=1.327e11):
        """Helper method to plot energy on specific axis."""
        all_energies = []
        time_points = []
        current_time = 0

        for solution in solutions:
            ke = 0.5 * (solution[:, 2] ** 2 + solution[:, 3] ** 2)
            r = np.sqrt(solution[:, 0] ** 2 + solution[:, 1] ** 2)
            pe = -gm_sun / r
            total_energy = ke + pe
            all_energies.extend(total_energy)

            segment_times = np.arange(current_time, current_time + len(total_energy))
            time_points.extend(segment_times)
            current_time += len(total_energy)

        ax.plot(time_points, all_energies, color="red", linewidth=1.5)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("Time (days)")
        ax.set_ylabel("Energy (km²/s²)")
        ax.set_title("Energy Profile")
