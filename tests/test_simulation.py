import pytest
import numpy as np
from datetime import datetime
from swingby.core.simulation import OrbitSimulation
from swingby.physics.constants import Config


class TestOrbitSimulation:
    def test_simulation_initialization(self):
        """Test that OrbitSimulation can be initialized."""
        sim = OrbitSimulation()
        assert sim is not None
        assert isinstance(sim.config, Config)

    def test_simulation_with_custom_config(self):
        """Test simulation initialization with custom config."""
        config = Config()
        sim = OrbitSimulation(config)
        assert sim.config is config

    def test_calculate_initial_velocity(self):
        """Test initial velocity calculation."""
        sim = OrbitSimulation()
        v_inf = 5.0

        v_sc_x, v_sc_y = sim.calculate_initial_velocity(v_inf)

        assert isinstance(v_sc_x, float)
        assert isinstance(v_sc_y, float)
        assert v_sc_x != 0
        assert v_sc_y != 0

    def test_setup_initial_conditions(self):
        """Test initial conditions setup."""
        sim = OrbitSimulation()
        dt_start = datetime(2022, 9, 23)
        v_inf = 5.0

        x0 = sim.setup_initial_conditions(dt_start, v_inf)

        assert isinstance(x0, np.ndarray)
        assert len(x0) == 4  # [x, y, vx, vy]
        assert not np.any(np.isnan(x0))

    def test_run_simulation(self):
        """Test running a basic simulation."""
        sim = OrbitSimulation()

        # Simple test parameters
        v_inf = 5.0
        dt_start = datetime(2022, 9, 23)
        travel_days = [30, 60]
        delta_V = [[0.0, 0.0], [-0.005, 0.0]]
        planet_list = ["venus", "earth"]

        # Run simulation
        sim.run_simulation(v_inf, dt_start, travel_days, delta_V, planet_list)

        # Check results
        assert len(sim.solutions) == 2
        assert sim.timeseries is not None
        assert sim.planet_coordinates is not None


