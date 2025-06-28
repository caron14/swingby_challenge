from datetime import datetime

import numpy as np
import pytest

from swingby.physics.constants import Config
from swingby.physics.dynamics import orbital_equation_of_motion_nbody


class TestEquationOfMotion:

    def test_nbody_equation_format(self):
        """Test that n-body equation returns correct format."""
        config = Config()
        x = np.array([1.0, 0.0, 0.0, 1.0])
        t = 0.0
        dt_start = datetime(2022, 1, 1)
        planet_list: list[str] = []

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
        planet_list: list[str] = []

        result = orbital_equation_of_motion_nbody(
            x, t, dt_start, planet_list, config.dict_GM, config.dict_planet_radius
        )

        # Should have negative acceleration in x direction (toward sun)
        assert result[2] < 0
        assert abs(result[3]) < 1e-10
