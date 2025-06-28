# Swingby Challenge

A spacecraft orbital mechanics simulation that models planetary swingby maneuvers using N-body gravitational interactions.

## Overview

This simulation calculates spacecraft trajectories through the solar system with gravity assists from Venus, Earth, and Mars. It uses real astronomical data and implements N-body gravitational dynamics to model realistic orbital mechanics.

## Installation

This project uses `uv` for dependency management. To set up the environment:

```bash
# Install dependencies
uv sync

# Add development dependencies (for testing and code quality)
uv add --dev pytest pytest-cov black isort flake8 mypy
```

## Quick Start

```bash
# Run the main simulation
uv run python main.py

# Or use the installed script
uv run swingby-sim

# Pluto mission example
uv run python pluto_mission.py

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.
```

## Dependencies

### Core Dependencies
- **numpy**: Numerical computations and array operations
- **matplotlib**: Plotting and visualization
- **scipy**: Scientific computing and ODE integration
- **astropy**: Astronomical calculations and ephemeris data (DE432s)
- **pandas**: Data manipulation and time series
- **jplephem**: JPL planetary ephemeris data

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Test coverage reporting
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Static type checking

## Usage

The main simulation is configured in `main.py` with parameters:
- `v_inf`: Spacecraft velocity relative to Earth (km/s)
- `start_date`: Mission start date
- `travel_days`: Duration of each trajectory segment
- `delta_V`: Velocity changes for orbital maneuvers
- `planet_list`: Planets to include in the simulation

## Output

The simulation generates:
- `output/orbit.png`: Spacecraft trajectory with planetary orbits
- `output/distance.png`: Distance between spacecraft and Earth over time

## Architecture

The codebase features both legacy and modern modular architecture:

### Modern Package Structure (swingby/)
- **swingby.core.simulation**: Main `OrbitSimulation` class and simulation orchestration
- **swingby.physics**: Physical modeling (constants, N-body dynamics)
- **swingby.utils**: Utility functions (coordinate transforms, ephemeris data)
- **swingby.visualization**: Plotting and output generation

### Legacy Files (for backward compatibility)
- **config.py**: Physical constants and planetary parameters
- **orbit.py**: Original simulation engine
- **equation_of_motion.py**: N-body gravitational dynamics
- **planet_position.py**: Planetary position calculations
- **utils.py**: Coordinate system transformations

### Key Features
- **N-body Dynamics**: Real planetary gravitational interactions
- **Real Ephemeris**: Uses JPL DE432s ephemeris data via astropy
- **Collision Detection**: Prevents spacecraft surface impacts
- **Modular Delta-V**: Instantaneous velocity changes between segments
- **Comprehensive Testing**: 29 tests covering numerical accuracy and integration

## Development

### Running Tests
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_simulation.py

# Run specific test
uv run pytest tests/test_simulation.py::TestOrbitSimulation::test_calculate_initial_velocity
```

### Code Quality
```bash
# Check formatting
uv run black --check .

# Format code
uv run black .

# Check imports
uv run isort --check-only .

# Sort imports
uv run isort .

# Lint code (excluding virtual environment)
uv run flake8 . --exclude=.venv

# Type checking
uv run mypy .
```

### Testing Notes
- All 29 tests should pass with current implementation
- Modern `swingby/` package has 87-94% test coverage
- Legacy files have 0% coverage but remain for compatibility
- Coordinate transformations use standard counter-clockwise rotation matrices