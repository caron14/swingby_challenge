import numpy as np


class Config:
    """
    物理定数とそれから決まる定数値
    """

    # 地球の公転軌道半径, km
    r_earth = 149597870.7  # 1天文単位を設定

    # 地球の公転速度, km/s <-- 軌道のE保存則から算出
    v_earth = np.sqrt(1.327e11 / r_earth)

    """
    重力定数
        * G: 万有引力定数(m^3*kg^{-1}*s^{-2})
        * M: 惑星質量(kg)
        --> GM: 重力定数(km^3*s^{-2})

    Ref.
        * https://ja.wikipedia.org/wiki/%E5%A4%A7%E3%81%8D%E3%81%95%E9%A0%86%E3%81%AE%E5%A4%AA%E9%99%BD%E7%B3%BB%E5%A4%A9%E4%BD%93%E3%81%AE%E4%B8%80%E8%A6%A7
    Note: Gは測定精度が低い一方で、GMは太陽や地球で測定精度が高い
    """
    G = 6.6743e-11 * 1e-9  # m^{-3} --> km^{-3}
    dict_GM = {
        "sun": 1.327e11,
        "mercury": G * 330.2e21,
        "venus": G * 4868.5e21,
        "earth": 398600.4354360959,
        "mars": G * 641.85e21,
        "jupiter": G * 1.8986e27,
        "saturn": G * 568460e21,
        "uranus": G * 86832e21,
        "neptune": G * 102430e21,
        "pluto": G * 13.105e21,
    }

    """
    惑星の平均半径(km)
    """
    dict_planet_radius = {
        "sun": 696000,
        "mercury": 2439.7,
        "venus": 6051.8,
        "earth": 6371,
        "mars": 3390,
        "jupiter": 69911,
        "saturn": 58232,
        "uranus": 25362,
        "neptune": 24622,
        "pluto": 1185,
    }


