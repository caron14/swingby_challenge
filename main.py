import os
from pathlib import Path

from config import Config
from orbit import spacecraft_orbit



def main():
    # currend work directory
    CWD_PATH = Path(os.path.dirname(__file__))
    # 結果出力フォルダ: 存在しない場合は作成する
    OUTPUT_PATH = CWD_PATH / 'output'
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # 物理定数とそれから決まる定数値
    config = Config()
    
    """
    実験条件
    """
    v_inf = 5.0  # 5.0
    t_twobody = 0.2  # 0.2
    t_Nbody = 2.9  # 2
    delta_t = 1 / 365
    delta_V = [0.0055, 0.]  # Vx, Vy, [0.0055, 0]

    """
    探査機の軌道伝搬の計算
    """
    spacecraft_orbit(
        config=config,
        OUTPUT_PATH=OUTPUT_PATH,
        v_inf=v_inf,
        t_twobody=t_twobody,
        t_Nbody=t_Nbody,
        delta_t=delta_t,
        delta_V=delta_V,
    )



if __name__ == "__main__":
    main()