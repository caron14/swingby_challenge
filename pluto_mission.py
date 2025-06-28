from datetime import datetime
import os
from pathlib import Path
import shutil

from swingby.physics.constants import Config
from swingby.core.simulation import OrbitSimulation


def main():
    cwd = Path(os.path.dirname(__file__))
    output_path = cwd / "output_pluto"
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()

    config = Config()
    sim = OrbitSimulation(config)

    v_inf = 5.0
    start_date = "2025-01-01"
    travel_days = [120, 220, 450, 2900]
    delta_v = [
        [0.0, 0.0],
        [0.4, -0.3],
        [-0.5, 0.2],
        [-1.2, 0.0],
    ]
    planet_list = ["venus", "mars", "jupiter", "pluto"]

    sim.run_simulation(
        v_inf=v_inf,
        dt_start=datetime.strptime(start_date, "%Y-%m-%d"),
        travel_days=travel_days,
        delta_V=delta_v,
        planet_list=planet_list,
    )

    if sim.total_delta_v > 5.0:
        raise ValueError("Total delta-V exceeds mission requirement")

    sim.save_results(output_path)


if __name__ == "__main__":
    main()
