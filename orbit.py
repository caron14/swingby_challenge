from datetime import datetime, timedelta
import os
from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

from utils import transform_to_rotating_coordinate_system
from equation_of_motion import orbital_equation_of_motion_twobody
from equation_of_motion import orbital_equation_of_motion_nbody



def spacecraft_orbit(
        config=None,
        OUTPUT_PATH=None,
        v_inf=None,
        dt_start=None,
        t_twobody=None,
        t_Nbody=None,
        delta_t=None,
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
        t_twobody(float): 二体問題での軌道伝播の期間, year
            Note: 探査機と地球の初期位置の一致で数値発散を回避するため
                  0 < t_twobody < 1
        num_step_in_t_twobody(int): 二体問題での軌道伝播の期間のステップ数
        t_Nbody(float): N体問題での軌道伝播の期間, year
            ex. 太陽-地球-探査機
        num_step_in_t_Nbody(int): N体問題での軌道伝播の期間のステップ数
        delta_V(list, float): delta_Vx, delta_Vy
            軌道制御(ΔV)による速度変化
    """

    """
    条件を取得
    """
    # 地球の公転軌道半径, km
    r_earth = config.r_earth
    # 地球の公転速度, km/s <-- 軌道のE保存則から算出
    v_earth = config.v_earth
    # 軌道制御(ΔV)による速度変化
    delta_Vx, delta_Vy = delta_V[0], delta_V[1]

    """
    探査機の公転速度 <-- 幾何学的に算出される(参考サイトを参照)
    """
    # x成分, km/s
    v_sc_x = np.sqrt(4 * v_earth**2 - v_inf**2) * v_inf / (2 * v_earth)
    # y成分, km/s
    v_sc_y = (2 * v_earth**2 - v_inf**2) / (2 * v_earth)

    # 回転座標へ変換
    omega, time = 2*np.pi / (1*365*24*60*60), np.array(0)
    v_sc_x, v_sc_y = transform_to_rotating_coordinate_system(
        x=v_sc_x, y=v_sc_y,
        omega=omega, time=np.array(0),
    )

    """
    0年〜{t_twobody}年の間の軌道伝播(太陽と探査機の二体問題)
    Note: 探査機と地球の初期位置が一致しているため、
          最初は太陽との二体問題で解かないと計算が発散する
    """
    x0 = np.array([r_earth, 0.0, -v_sc_x, v_sc_y])  # 位置(km), 速度(km/s)

    num_step = int(t_twobody / delta_t)
    t_span_twobody = np.linspace(0, t_twobody*365*24*60*60, num_step)
    # (x, y, vx, vy) --> (time step, each coord and velocity components)
    sol_0to1 = odeint(orbital_equation_of_motion_twobody, x0, t_span_twobody)

    """
    {t_twobody}年〜{t_Nbody}年の間の軌道伝播(N体問題)
    """
    # 軌道伝播された位置・速度に軌道制御(ΔV)を加える
    x1 = sol_0to1[-1, :] + [0, 0, delta_Vx, delta_Vy]

    num_step = int(t_Nbody / delta_t)
    # tot_time = t_Nbody*365*24*60*60 - t_twobody*365*24*60*60  # (sec): year to sec
    # {t_twobody}年〜{t_Nbody}年分を200ステップで刻む
    t_span_Nbody = np.linspace(t_twobody*365*24*60*60, t_Nbody*365*24*60*60, num_step)
    sol_1to2 = odeint(orbital_equation_of_motion_nbody,
                      x1, t_span_Nbody, 
                      args=(dt_start, planet_list, config.dict_GM, config.dict_planet_radius))  # argsの要素が1つの時は ","を忘れないこと


    # 地球の軌道
    omega = 2*np.pi / (1*365*24*60*60)  # 2*pi / T
    t_span_tot = np.concatenate([t_span_twobody, t_span_Nbody], axis=0)
    x_e = r_earth*np.cos(omega*t_span_tot)
    y_e = r_earth*np.sin(omega*t_span_tot)
    vx_e = -omega*r_earth*np.sin(omega*t_span_tot)
    vy_e = omega*r_earth*np.cos(omega*t_span_tot)


    """
    軌道の描画
    """
    # 回転座標へ変換に必要な情報
    omega = 2*np.pi / (1*365*24*60*60)

    fig = plt.figure(figsize=(6, 6))
    # Sun
    plt.scatter(0, 0, color='orange', s=200, label='Sun')
    # Earth
    # theta = np.linspace(0, 2*np.pi, 100)
    # plt.plot(r_earth*np.cos(theta), r_earth*np.sin(theta), 
    #          color='blue', linestyle='--', label="Earth")
    plt.plot(x_e, y_e, color='blue', linestyle='--', label="Earth")
    # Spacecraft: 0 ~ {t_twobody}
    # _x, _y = transform_to_rotating_coordinate_system(
    #     x=sol_0to1[:, 0], y=sol_0to1[:, 1],
    #     omega=omega, time=t_span_twobody,
    # )
    # plt.plot(_x, _y, color='red', label="two-body problem")
    plt.plot(sol_0to1[:, 0], sol_0to1[:, 1], color='red', label="two-body problem")
    # Spacecraft: 0 ~ {t_Nbody}
    # _x, _y = transform_to_rotating_coordinate_system(
    #     x=sol_1to2[:, 0], y=sol_1to2[:, 1],
    #     omega=omega, time=t_span_Nbody,
    # )
    # plt.plot(_x, _y, color='green', label="N-body problem")
    plt.plot(sol_1to2[:, 0], sol_1to2[:, 1], color='green', label="N-body problem")
    plt.grid()  # 格子をつける
    plt.legend(bbox_to_anchor=(0.5, 1.025))  # loc="lower left"
    plt.gca().set_aspect('equal')  # グラフのアスペクト比を揃える
    plt.xlabel('x, km')
    plt.ylabel('y, km')
    plt.savefig(OUTPUT_PATH / 'orbit.png')
    plt.show()
    plt.close(fig)



if __name__ == "__main__":
    pass