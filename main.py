import os
import shutil
from datetime import datetime
from pathlib import Path

from swingby.core.simulation import spacecraft_orbit
from swingby.physics.constants import Config


def main():
    # currend work directory
    CWD_PATH = Path(os.path.dirname(__file__))
    # 結果出力フォルダ: 存在しない場合は作成する
    OUTPUT_PATH = CWD_PATH / "output"
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    else:
        # 過去の結果を削除
        shutil.rmtree(OUTPUT_PATH)
        os.makedirs(OUTPUT_PATH)

    # 物理定数とそれから決まる定数値
    config = Config()

    """
    実験条件
    """
    v_inf = 5.0  # 5.0
    start_date = "2025-01-01"  # Adjusted start date for better alignment
    travel_days = [
        150,  # Earth to Venus
        280,  # Venus to Mars
        620,  # Mars to Jupiter
        2900, # Jupiter to Pluto (long travel time)
    ]
    delta_V = [
        [0.0, 0.0],  # Earth to Venus (initial launch, no delta_V here)
        [0.5, -0.5],  # Venus to Mars
        [-0.75, 0.35],  # Mars to Jupiter
        [0.55, 0.15],  # Jupiter to Pluto
    ]
    planet_list = ["venus", "mars", "jupiter", "pluto"]

    """
    探査機の軌道伝搬の計算
    """
    spacecraft_orbit(
        config=config,
        OUTPUT_PATH=OUTPUT_PATH,
        v_inf=v_inf,
        dt_start=datetime.strptime(start_date, "%Y-%m-%d"),
        travel_days=travel_days,
        delta_V=delta_V,
        planet_list=planet_list,
    )


if __name__ == "__main__":
    main()
