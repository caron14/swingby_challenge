from datetime import datetime, timedelta
import os
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from astropy.time import Time
from astropy.coordinates import get_body_barycentric

from utils import transform_to_rotating_coordinate_system
from equation_of_motion import orbital_equation_of_motion_twobody
from equation_of_motion import orbital_equation_of_motion_nbody
from planet_position import get_planet_coord_timeseries


def spacecraft_orbit(
    config=None,
    OUTPUT_PATH=None,
    v_inf=None,
    dt_start=None,
    travel_days=None,
    delta_V=None,
    planet_list=None,
):
    """
    探査機の軌道

    Args:
        config(class): 物理定数とそれから決まる定数値
        OUTPUT_PATH: 出力先のPATH
        v_inf(float): 地球公転速度に対する探査機の相対速度V∞, km/s
            Note: ロケット打ち上げ能力に依存し、今回は v_inf < 5km/s を仮定
        dt_start(datetime): 打ち上げ時刻情報
        delta_V(list, float): delta_Vx, delta_Vy
            軌道制御(ΔV)による速度変化
        planet_list(list): 惑星リスト
    """

    """
    条件を取得
    """
    # 地球の公転軌道半径, km
    r_earth = config.r_earth
    # 地球の公転速度, km/s <-- 軌道のE保存則から算出
    v_earth = config.v_earth

    """
    探査機の公転速度 <-- 幾何学的に算出される(参考サイトを参照)
    """
    # x成分, km/s
    v_sc_x = np.sqrt(4 * v_earth**2 - v_inf**2) * v_inf / (2 * v_earth)
    # y成分, km/s
    v_sc_y = (2 * v_earth**2 - v_inf**2) / (2 * v_earth)

    """
    0年〜{t_Nbody}年の間の軌道伝播(N体問題)
        * 軌道伝播中の位置・速度に軌道制御(ΔV)を加える
    """
    # 初期の位置(km), 速度(km/s)
    earth_coord_init = get_body_barycentric("earth", Time(dt_start))
    _x_e, _y_e = np.array(earth_coord_init.x), np.array(earth_coord_init.y)
    x0 = np.array(
        [_x_e + 1 * config.dict_planet_radius["earth"], _y_e, -v_sc_x, v_sc_y]
    )
    # x0 = np.array([_x_e + 1*config.dict_planet_radius['earth'], _y_e, 0., 1.29*config.v_earth])

    solutions = []
    for i, (_travel_days, _delta_V) in enumerate(zip(travel_days, delta_V)):
        if i == 0:
            # スタート時
            t_span_sec = np.arange(
                0, _travel_days * 24 * 60 * 60, 24 * 60 * 60, dtype=np.int64
            )
            _planet_list = []
            solution = odeint(
                orbital_equation_of_motion_nbody,
                x0,
                t_span_sec,
                args=(
                    dt_start,
                    _planet_list,
                    config.dict_GM,
                    config.dict_planet_radius,
                ),
            )  # argsの要素が1つの時は ","を忘れないこと
            solutions.append(solution)
            dt_next = dt_start + timedelta(days=_travel_days - 1)
            _t = t_span_sec[-1]
        else:
            # 軌道制御(ΔV)による速度変化
            x0 = solution[-1, :] + [0, 0, _delta_V[0], _delta_V[1]]

            t_span_sec = np.arange(
                _t, _t + _travel_days * 24 * 60 * 60, 24 * 60 * 60, dtype=np.int64
            )
            solution = odeint(
                orbital_equation_of_motion_nbody,
                x0,
                t_span_sec,
                args=(dt_start, planet_list, config.dict_GM, config.dict_planet_radius),
            )  # argsの要素が1つの時は ","を忘れないこと
            solutions.append(solution)
            dt_next += timedelta(days=_travel_days - 1)
            _t = t_span_sec[-1]

    # 基準日からの飛行時間
    dt_next = dt_start + timedelta(days=sum(travel_days) - 1)
    timeseries = pd.date_range(dt_start, dt_next, freq="D")
    # 基準日から飛行時間での各惑星の座標
    dict_planet_coord_timeseries = get_planet_coord_timeseries(timeseries, planet_list)
    # 軌道の描画
    fig = plt.figure(figsize=(6, 6))
    # Sun
    plt.scatter(0, 0, color="orange", s=200, label="Sun")
    # # Earthの初期値 _x_e, _y_e
    # plt.scatter(_x_e, _y_e, color='red')
    # 各惑星
    for _planet in dict_planet_coord_timeseries.keys():
        _x = dict_planet_coord_timeseries[_planet]["x"]
        _y = dict_planet_coord_timeseries[_planet]["y"]
        # plot
        plt.plot(_x, _y, label=_planet, linewidth=2)
        plt.scatter(_x[-1], _y[-1], s=40)  # final point
        # 探査機と地球間の距離
        if _planet == "earth":
            _x_sc = np.concatenate([_solution[:, 0] for _solution in solutions])
            _y_sc = np.concatenate([_solution[:, 1] for _solution in solutions])
            distance = np.sqrt(np.power((_x - _x_sc), 2) + np.power((_y - _y_sc), 2))
    # 探査機
    for _solution in solutions:
        plt.plot(_solution[:, 0], _solution[:, 1], color="black")
    plt.scatter(
        solutions[-1][-1, 0], solutions[-1][-1, 1], color="black", label="spacecraft"
    )
    plt.grid()  # 格子をつける
    plt.legend(bbox_to_anchor=(0.75, 0.9))  # loc="lower left"
    plt.gca().set_aspect("equal")  # グラフのアスペクト比を揃える
    plt.xlabel("x, km")
    plt.ylabel("y, km")
    plt.savefig(OUTPUT_PATH / "orbit.png")
    plt.close(fig)

    # 探査機と地球間の距離
    fig = plt.figure(figsize=(6, 6))
    plt.plot(timeseries, distance, color="black")
    plt.savefig(OUTPUT_PATH / "distance.png")
    plt.close(fig)


if __name__ == "__main__":
    pass
