# Swingby Challenge

A spacecraft orbital mechanics simulation that models planetary swingby maneuvers using N-body gravitational interactions.

## Overview

This simulation calculates spacecraft trajectories through the solar system with gravity assists from Venus, Earth, and Mars. It uses real astronomical data and implements N-body gravitational dynamics to model realistic orbital mechanics.

## Installation

This project uses `uv` for dependency management. To set up the environment:

```bash
# Install dependencies
uv sync

# Run the simulation
uv run python main.py
```

## Dependencies

- numpy: Numerical computations
- matplotlib: Plotting and visualization
- scipy: Scientific computing and ODE integration
- astropy: Astronomical calculations and ephemeris data
- pandas: Data manipulation

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

- **config.py**: Physical constants and planetary parameters
- **orbit.py**: Main simulation engine with orbital integration
- **equation_of_motion.py**: N-body gravitational dynamics
- **planet_position.py**: Real planetary position calculations using astropy
- **utils.py**: Coordinate system transformations