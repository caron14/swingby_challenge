import pytest

from swingby.physics.constants import Config


class TestConfig:
    def test_config_initialization(self):
        """Test that Config class can be initialized."""
        config = Config()
        assert config is not None

    def test_earth_orbital_radius(self):
        """Test that Earth's orbital radius is set correctly."""
        config = Config()
        assert config.r_earth == 149597870.7

    def test_earth_orbital_velocity(self):
        """Test that Earth's orbital velocity is calculated correctly."""
        config = Config()
        assert config.v_earth > 0
        # Approximate Earth's orbital velocity should be around 29.8 km/s
        assert 25 < config.v_earth < 35

    def test_gravitational_parameters(self):
        """Test that gravitational parameters are defined for major planets."""
        config = Config()
        required_bodies = ["sun", "mercury", "venus", "earth", "mars", "jupiter"]

        for body in required_bodies:
            assert body in config.dict_GM
            assert config.dict_GM[body] > 0

    def test_planetary_radii(self):
        """Test that planetary radii are defined for major planets."""
        config = Config()
        required_bodies = ["sun", "mercury", "venus", "earth", "mars", "jupiter"]

        for body in required_bodies:
            assert body in config.dict_planet_radius
            assert config.dict_planet_radius[body] > 0

    def test_earth_gm_value(self):
        """Test that Earth's GM value is reasonable."""
        config = Config()
        # Earth's GM should be around 398600 km³/s²
        assert 300000 < config.dict_GM["earth"] < 500000
