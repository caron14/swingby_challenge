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
    Project Pluto Pioneer v2.0 - 高エネルギー冥王星探査軌道
    
    修正戦略 (New Horizons実績ベース):
    - Venus スイングバイ: 主要脱出加速 (近日点最大推力)
    - Mars スイングバイ: 軌道修正 + 追加エネルギー
    - Jupiter スイングバイ: 重力アシスト最大化
    - 総飛行時間: ~13年 (現実的な高エネルギー軌道)
    """
    v_inf = 5.0  # km/s - 打上げ時の地球相対速度
    start_date = "2025-01-15"  # 最適な惑星配置を考慮した打上げ日
    
    # 修正軌道セグメント (高エネルギー軌道対応)
    travel_days = [
        120,    # Earth → Venus (4ヶ月, 短縮で効率化)
        400,    # Venus → Mars (13ヶ月, 高速軌道)
        800,    # Mars → Jupiter (26ヶ月, 重力アシスト最適化) 
        3200,   # Jupiter → Pluto (8.8年, 高速外惑星軌道)
    ]
    
    # 制約内最大効率ΔV配分 (総計 = 5.0 km/s)
    delta_V = [
        [2.2, 0.0],   # Venus: 主要脱出推力 (2.2 km/s)
        [1.0, 0.7],   # Mars: 軌道修正 + 加速 (1.22 km/s)
        [0.9, 0.4],   # Jupiter: 重力アシスト調整 (0.98 km/s)
        [0.4, 0.2],   # Pluto: 最終調整 (0.45 km/s)
    ]
    # 総ΔV = 2.20 + 1.22 + 0.98 + 0.45 = 4.85 km/s < 5.0 km/s ✓
    # Venus近日点での大幅加速により太陽系外縁部到達エネルギーを獲得
    
    planet_list = ["earth", "venus", "mars", "jupiter", "pluto"]

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
