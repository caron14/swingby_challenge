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
    num_step_in_t_twobody = 200  # 200
    t_Nbody = 1.75  # 2
    num_step_in_t_Nbody = 200  # 200
    delta_V = [0.0055, 0.]  # Vx, Vy, [0.0055, 0]

    """
    探査機の軌道伝搬の計算
    """
    spacecraft_orbit(
        config=config,
        OUTPUT_PATH=OUTPUT_PATH,
        v_inf=v_inf,
        t_twobody=t_twobody,
        num_step_in_t_twobody=num_step_in_t_twobody,
        t_Nbody=t_Nbody,
        num_step_in_t_Nbody=num_step_in_t_Nbody,
        delta_V=delta_V,
    )



if __name__ == "__main__":
    main()