"""
Swingby Challenge - Spacecraft Orbital Mechanics Simulation

A modular package for simulating spacecraft trajectories with planetary swingby maneuvers.
"""

__version__ = "0.1.0"
__author__ = "sho"

from .core.simulation import OrbitSimulation
from .physics.constants import Config
from .physics.dynamics import orbital_equation_of_motion_twobody, orbital_equation_of_motion_nbody
from .utils.coordinates import transform_to_rotating_coordinate_system
from .utils.ephemeris import get_planet_coord, get_planet_coord_timeseries

__all__ = [
    "OrbitSimulation",
    "Config",
    "orbital_equation_of_motion_twobody",
    "orbital_equation_of_motion_nbody", 
    "transform_to_rotating_coordinate_system",
    "get_planet_coord",
    "get_planet_coord_timeseries",
]