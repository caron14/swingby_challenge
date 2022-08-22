import sys

import numpy as np



# def orbital_equation_of_motion(x, t, GM=1.327e11):
#     """
#     軌道の運動方程式
    
#     Args:
#         x(ndarray): 天体の位置, km
#         t(ndarray): 時刻ステップの配列
#         GM(float): 万有引力定数×中心天体の質量, km^3/s^(-2)
#             Defaultは太陽質量の値
#     Return:
#         dxdt: 4次元ベクトル(位置と速度ベクトルの時間微分)
#             1, 2成分: 位置ベクトルの時間微分(dr/dt)
#             3, 4成分: 速度ベクトルの時間微分(dv/dt)
#     """
#     # 中心天体からの距離
#     r_norm = np.sqrt(x[0]**2 + x[1]**2)
#     # [dr_x/dt, dr_y/dt, dv_x/dt, dv_y/dt]
#     dxdt = [x[2], 
#             x[3], 
#             -GM*x[0]/(r_norm**3),
#             -GM*x[1]/(r_norm**3)]
    
#     return dxdt


def orbital_equation_of_motion_twobody(x, t):
    """
    二体問題の運動方程式

    Args:
        x(ndarray): 天体の位置, km
        t(ndarray): 時刻ステップの配列
        GM(float): 万有引力定数×太陽の質量, km^3/s^(-2)
    """
    GM = 1.327e11 # 万有引力定数×中心天体の質量, km^3/s^(-2)
    r_norm = np.sqrt(x[0]**2 + x[1]**2)	
    dxdt = [x[2],
            x[3],
            -GM*x[0]/(r_norm**3),
            -GM*x[1]/(r_norm**3)]
    
    return dxdt


def orbital_equation_of_motion_nbody(
        x,
        t,
        dt_start,
        planet_list,
    ):
    """
    N体の軌道の運動方程式
    Note: 円運動の仮定に注意
    
    Args:
        x(ndarray): 天体の位置, km
        t(ndarray): 時刻ステップの配列
        dt_start(datetime): 打ち上げ時刻情報

        GM(float): 万有引力定数×太陽の質量, km^3/s^(-2)
        GM1(float): 万有引力定数×地球の質量, km^3/s^(-2)
        period1(float): 地球の軌道周期, sec
        a1(float): 地球の軌道長半径, km
    """
    # 条件設定
    GM=1.327e11
    GM1=3.986e5

    # 各惑星位置の取得
    dt_next = dt_start + timedelta(days=round(t))
    dict_planet_coord = get_planet_coord(dt_next, planet_list)

    # 地球の位置
    period1 = 365*24*60*60
    a1 = 149597870.7
    r1 = np.array([a1*np.cos(2*np.pi*t/period1 + theta1), 
                   a1*np.sin(2*np.pi*t/period1 + theta1)])

    # 運動方程式の計算
    d1 = x[0:2] - r1
    r_norm = np.sqrt(x[0]**2 + x[1]**2)
    d1_norm = np.sqrt(d1[0]**2 + d1[1]**2)

    if d1_norm < 6371: #　地球距離が地球半径以下になると衝突してしまうため、エラーを返す
        print("ERROR: 地球スイングバイ時の高度がマイナスです！")
        sys.exit()

    dxdt = [x[2],
            x[3],
            -GM*x[0]/(r_norm**3) - GM1*d1[0]/(d1_norm**3),
            -GM*x[1]/(r_norm**3) - GM1*d1[1]/(d1_norm**3)]

    return dxdt



if __name__ == "__main__":
    pass