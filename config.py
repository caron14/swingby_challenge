import numpy as np



class Config:
    """
    物理定数とそれから決まる定数値
    """
    # 地球の公転軌道半径, km
    r_earth = 149597870.7  # 1天文単位を設定

    # 地球の公転速度, km/s <-- 軌道のE保存則から算出
    v_earth = np.sqrt(1.327e11 / r_earth)





if __name__ == "__main__":
    pass