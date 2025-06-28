import pytest
import numpy as np
from datetime import datetime
from swingby.physics.dynamics import orbital_equation_of_motion_twobody, orbital_equation_of_motion_nbody
from swingby.physics.constants import Config


class TestEquationOfMotion:
    def test_twobody_equation_format(self):
        """Test that two-body equation returns correct format."""
        x = np.array([1.0, 0.0, 0.0, 1.0])  # position and velocity
        t = 0.0
        
        result = orbital_equation_of_motion_twobody(x, t)
        
        # Should return 4-element array [dx/dt, dy/dt, dvx/dt, dvy/dt]
        assert len(result) == 4
        assert isinstance(result, list)

    def test_twobody_velocity_derivative(self):
        """Test that velocity components are returned correctly."""
        x = np.array([1.0, 2.0, 3.0, 4.0])  # [x, y, vx, vy]
        t = 0.0
        
        result = orbital_equation_of_motion_twobody(x, t)
        
        # First two elements should be velocity components
        assert result[0] == 3.0  # dx/dt = vx
        assert result[1] == 4.0  # dy/dt = vy

    def test_twobody_acceleration_direction(self):
        """Test that acceleration points toward center."""
        # Position at (1, 0) should have acceleration in -x direction
        x = np.array([1.0, 0.0, 0.0, 0.0])
        t = 0.0
        
        result = orbital_equation_of_motion_twobody(x, t)
        
        # Acceleration in x should be negative (toward center)
        assert result[2] < 0
        # Acceleration in y should be zero
        assert abs(result[3]) < 1e-10

    def test_nbody_equation_format(self):
        """Test that n-body equation returns correct format."""
        config = Config()
        x = np.array([1.0, 0.0, 0.0, 1.0])
        t = 0.0
        dt_start = datetime(2022, 1, 1)
        planet_list = []
        
        result = orbital_equation_of_motion_nbody(
            x, t, dt_start, planet_list, config.dict_GM, config.dict_planet_radius
        )
        
        # Should return 4-element array
        assert len(result) == 4
        assert isinstance(result, np.ndarray)

    def test_nbody_with_empty_planet_list(self):
        """Test n-body equation with no planets (should behave like two-body)."""
        config = Config()
        x = np.array([1.0, 0.0, 0.0, 0.0])
        t = 0.0
        dt_start = datetime(2022, 1, 1)
        planet_list = []
        
        result = orbital_equation_of_motion_nbody(
            x, t, dt_start, planet_list, config.dict_GM, config.dict_planet_radius
        )
        
        # Should have negative acceleration in x direction (toward sun)
        assert result[2] < 0
        assert abs(result[3]) < 1e-10