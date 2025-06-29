"""
Core simulation functionality for spacecraft orbital mechanics.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from astropy.time import Time
from astropy.coordinates import get_body_barycentric

from ..physics.constants import Config
from ..physics.dynamics import orbital_equation_of_motion_nbody
from ..utils.ephemeris import get_planet_coord_timeseries
from ..visualization.plots import OrbitPlotter


class OrbitSimulation:
    """
    Spacecraft orbital mechanics simulation with planetary swingby maneuvers.

    This class handles the complete simulation workflow including:
    - Initial conditions setup
    - Orbital propagation with N-body dynamics
    - Delta-V maneuvers
    - Visualization and output
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the orbit simulation.

        Args:
            config: Physical constants configuration. If None, creates default Config.
        """
        self.config = config or Config()
        self.plotter = OrbitPlotter()
        self.solutions = []
        self.timeseries = None
        self.planet_coordinates = None
        self.spacecraft_earth_distance = None

    def calculate_initial_velocity(self, v_inf: float) -> Tuple[float, float]:
        """
        Calculate initial spacecraft velocity components for escape trajectory.

        Args:
            v_inf: Spacecraft velocity relative to Earth (km/s)

        Returns:
            Tuple of (v_sc_x, v_sc_y) velocity components in km/s
        """
        v_earth = self.config.v_earth

        # 高エネルギー脱出軌道用の修正計算
        # 地球軌道速度 + 脱出用余剰速度
        v_sc_x = -(v_earth + v_inf)  # 負方向で高速脱出
        v_sc_y = v_inf * 0.5  # y成分で軌道調整

        return v_sc_x, v_sc_y

    def setup_initial_conditions(self, dt_start: datetime, v_inf: float) -> np.ndarray:
        """
        Setup initial position and velocity conditions.

        Args:
            dt_start: Mission start date
            v_inf: Spacecraft velocity relative to Earth (km/s)

        Returns:
            Initial state vector [x, y, vx, vy] in km and km/s
        """
        # Get Earth's initial position
        earth_coord_init = get_body_barycentric("earth", Time(dt_start))
        x_e, y_e = np.array(earth_coord_init.x), np.array(earth_coord_init.y)

        # Calculate spacecraft initial velocity
        v_sc_x, v_sc_y = self.calculate_initial_velocity(v_inf)

        # Initial state: position offset from Earth + velocity
        x0 = np.array(
            [x_e + 1 * self.config.dict_planet_radius["earth"], y_e, v_sc_x, v_sc_y]
        )

        return x0

    def propagate_orbit_segment(
        self,
        x0: np.ndarray,
        travel_days: int,
        t_start: int,
        dt_start: datetime,
        planet_list: List[str],
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Propagate orbit for a single segment.

        Args:
            x0: Initial state vector
            travel_days: Duration in days
            t_start: Start time in seconds
            dt_start: Mission start datetime
            planet_list: List of planets to include in dynamics

        Returns:
            Tuple of (solution_array, time_array)
        """
        t_span_sec = np.arange(
            t_start, t_start + travel_days * 24 * 60 * 60, 24 * 60 * 60, dtype=np.int64
        )

        solution = odeint(
            orbital_equation_of_motion_nbody,
            x0,
            t_span_sec,
            args=(
                dt_start,
                planet_list,
                self.config.dict_GM,
                self.config.dict_planet_radius,
            ),
        )

        return solution, t_span_sec

    def run_simulation(
        self,
        v_inf: float,
        dt_start: datetime,
        travel_days: List[int],
        delta_V: List[List[float]],
        planet_list: List[str],
    ) -> None:
        """
        Run the complete orbital simulation.

        Args:
            v_inf: Spacecraft velocity relative to Earth (km/s)
            dt_start: Mission start date
            travel_days: List of segment durations in days
            delta_V: List of velocity changes [delta_Vx, delta_Vy] for each segment
            planet_list: List of planets to include in simulation
        """
        # Setup initial conditions
        x0 = self.setup_initial_conditions(dt_start, v_inf)

        # Clear previous results
        self.solutions = []

        # Propagate each segment
        t_current = 0
        for i, (_travel_days, _delta_V) in enumerate(zip(travel_days, delta_V)):
            if i == 0:
                # First segment - no planets initially
                _planet_list = []
            else:
                # Apply delta-V maneuver
                x0 = self.solutions[-1][-1, :] + [0, 0, _delta_V[0], _delta_V[1]]
                _planet_list = planet_list

            solution, t_span = self.propagate_orbit_segment(
                x0, _travel_days, t_current, dt_start, _planet_list
            )

            self.solutions.append(solution)
            t_current = t_span[-1]

        # Generate time series and planet coordinates
        dt_end = dt_start + timedelta(days=sum(travel_days) - 1)
        self.timeseries = pd.date_range(dt_start, dt_end, freq="D")
        self.planet_coordinates = get_planet_coord_timeseries(
            self.timeseries, planet_list
        )

        # Calculate spacecraft-Earth distance
        self._calculate_spacecraft_earth_distance()

    def _calculate_spacecraft_earth_distance(self) -> None:
        """Calculate distance between spacecraft and Earth over time."""
        if "earth" in self.planet_coordinates:
            earth_x = self.planet_coordinates["earth"]["x"]
            earth_y = self.planet_coordinates["earth"]["y"]

            # Concatenate spacecraft positions
            sc_x = np.concatenate([sol[:, 0] for sol in self.solutions])
            sc_y = np.concatenate([sol[:, 1] for sol in self.solutions])

            # Calculate distance
            self.spacecraft_earth_distance = np.sqrt(
                np.power((earth_x - sc_x), 2) + np.power((earth_y - sc_y), 2)
            )

    def save_results(self, output_path: Union[str, Path]) -> None:
        """
        Save simulation results as plots.

        Args:
            output_path: Directory path to save output files
        """
        if not self.solutions:
            raise ValueError("No simulation results to save. Run simulation first.")

        output_path = Path(output_path)
        output_path.mkdir(exist_ok=True)

        # Save orbit plot
        self.plotter.plot_orbit(
            self.solutions, self.planet_coordinates, save_path=output_path / "orbit.png"
        )

        # Save distance plot
        if self.spacecraft_earth_distance is not None:
            self.plotter.plot_distance(
                self.timeseries,
                self.spacecraft_earth_distance,
                save_path=output_path / "distance.png",
            )



def spacecraft_orbit(
    config=None,
    OUTPUT_PATH=None,
    v_inf=None,
    dt_start=None,
    travel_days=None,
    delta_V=None,
    planet_list=None,
):
    """
    Legacy function wrapper for backward compatibility.

    This function maintains the original API while using the new modular structure.
    """
    simulation = OrbitSimulation(config)

    simulation.run_simulation(
        v_inf=v_inf,
        dt_start=dt_start,
        travel_days=travel_days,
        delta_V=delta_V,
        planet_list=planet_list,
    )

    simulation.save_results(OUTPUT_PATH)
