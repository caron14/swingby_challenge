import numpy as np
import pytest

from swingby.utils.coordinates import transform_to_rotating_coordinate_system


class TestUtils:
    def test_rotating_coordinate_transform_zero_time(self):
        """Test coordinate transformation with zero time."""
        x = np.array([1.0, 2.0])
        y = np.array([3.0, 4.0])
        omega = 1.0
        time = np.array([0.0, 0.0])

        x_rot, y_rot = transform_to_rotating_coordinate_system(x, y, omega, time)

        # At t=0, rotation should be identity
        np.testing.assert_array_almost_equal(x_rot, x)
        np.testing.assert_array_almost_equal(y_rot, y)

    def test_rotating_coordinate_transform_quarter_rotation(self):
        """Test coordinate transformation with quarter rotation."""
        x = np.array([1.0])
        y = np.array([0.0])
        omega = 1.0
        time = np.array([np.pi / 2])  # Quarter rotation

        x_rot, y_rot = transform_to_rotating_coordinate_system(x, y, omega, time)

        # After π/2 rotation, (1,0) should become (0,1)
        np.testing.assert_array_almost_equal(x_rot, [0.0], decimal=10)
        np.testing.assert_array_almost_equal(y_rot, [1.0], decimal=10)

    def test_rotating_coordinate_transform_half_rotation(self):
        """Test coordinate transformation with half rotation."""
        x = np.array([1.0])
        y = np.array([0.0])
        omega = 1.0
        time = np.array([np.pi])  # Half rotation

        x_rot, y_rot = transform_to_rotating_coordinate_system(x, y, omega, time)

        # After π rotation, (1,0) should become (-1,0)
        np.testing.assert_array_almost_equal(x_rot, [-1.0], decimal=10)
        np.testing.assert_array_almost_equal(y_rot, [0.0], decimal=10)

    def test_rotating_coordinate_transform_multiple_points(self):
        """Test coordinate transformation with multiple time points."""
        x = np.array([1.0, 1.0])
        y = np.array([0.0, 0.0])
        omega = 1.0
        time = np.array([0.0, np.pi])

        x_rot, y_rot = transform_to_rotating_coordinate_system(x, y, omega, time)

        # First point should remain (1,0), second should become (-1,0)
        expected_x = np.array([1.0, -1.0])
        expected_y = np.array([0.0, 0.0])

        np.testing.assert_array_almost_equal(x_rot, expected_x, decimal=10)
        np.testing.assert_array_almost_equal(y_rot, expected_y, decimal=10)
