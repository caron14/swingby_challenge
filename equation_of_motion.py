from datetime import datetime, timedelta
import sys

import numpy as np

from planet_position import get_planet_coord


def orbital_equation_of_motion_nbody(
    x,
    t,
    dt_start,
    planet_list,
    dict_GM,
    dict_planet_radius,
):
    """
    N体の軌道の運動方程式
    Note: 円運動の仮定に注意

    Args:
        x(ndarray): 天体の位置, km
        t(ndarray): 時刻ステップの配列, (day)
        dt_start(datetime): 打ち上げ時刻情報
        planet_list(list):
        dict_GM(dict): 重力定数(km^3*s^{-2})の辞書
        dict_planet_radius(dict): 惑星半径(km)の辞書
    """
    # 各惑星位置の取得
    passed_days = t / (24 * 60 * 60)
    dt_this_step = dt_start + timedelta(days=passed_days)
    dict_planet_coord = get_planet_coord(dt_this_step, planet_list)

    # 各惑星位置の位置ベクトル
    dxdt = np.zeros(4)
    for _planet in dict_planet_coord.keys():
        # 重力定数(km^3*s^{-2})
        _GM = dict_GM[_planet]

        # 惑星の位置ベクトル
        _r = np.array(
            [
                np.array(dict_planet_coord[_planet]["x"]),
                np.array(dict_planet_coord[_planet]["y"]),
            ]
        )
        # 探査機と惑星間の相対位置ベクトル
        _d = x[0:2] - _r
        # 相対位置ベクトルのノルム
        _d_norm = np.sqrt(_d[0] ** 2 + _d[1] ** 2)
        # Errorチェック <-- スイングバイ時に惑星と衝突する場合
        if _d_norm < dict_planet_radius[_planet]:
            print(f"ERROR: {_planet}でスイングバイ時の高度がマイナスです！")
            sys.exit()

        # main target
        dxdt[2] -= _GM * _d[0] / (_d_norm**3)
        dxdt[3] -= _GM * _d[1] / (_d_norm**3)

    # 探査機の位置ベクトルのノルム
    r_norm = np.sqrt(x[0] ** 2 + x[1] ** 2)

    # 追加
    dxdt[0] = x[2]
    dxdt[1] = x[3]
    dxdt[2] -= dict_GM["sun"] * x[0] / (r_norm**3)
    dxdt[3] -= dict_GM["sun"] * x[1] / (r_norm**3)

    return dxdt


"""
Ref.
"""


def orbital_equation_of_motion_twobody(x, t):
    """
    二体問題の運動方程式

    Args:
        x(ndarray): 天体の位置, km
        t(ndarray): 時刻ステップの配列
        GM(float): 万有引力定数×太陽の質量, km^3/s^(-2)
    """
    GM = 1.327e11  # 万有引力定数×中心天体の質量, km^3/s^(-2)
    r_norm = np.sqrt(x[0] ** 2 + x[1] ** 2)
    dxdt = [x[2], x[3], -GM * x[0] / (r_norm**3), -GM * x[1] / (r_norm**3)]

    return dxdt


if __name__ == "__main__":
    pass
