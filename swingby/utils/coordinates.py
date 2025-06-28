import numpy as np


def transform_to_rotating_coordinate_system(
    x=None,
    y=None,
    omega=None,
    time=None,
):
    """
    回転座標系へ変換

    Args:
        x, y(ndarray): x, y成分の物理量(座標と速度)
        omega(float): 角速度, [1/sec]
        time(ndarray): 時間, [sec]
    """
    phase = float(omega) * np.array(time)

    # 変換 (標準的な反時計回り回転行列)
    x_rot = x * np.cos(phase) - y * np.sin(phase)
    y_rot = x * np.sin(phase) + y * np.cos(phase)

    return x_rot, y_rot


