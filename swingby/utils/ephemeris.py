import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris  # , EarthLocation
from astropy.coordinates import get_body_barycentric

solar_system_ephemeris.set("de432s")


def get_planet_coord(timestamp, planet_list):
    """
    指定の時刻と惑星の座標を取得

    Return: dict
        key: planet name
        value: dict(x, y, x)
            座標値(km)
    """

    def _get_planet_coord_list(timestamp, planet_list):
        """
        指定時刻の指定惑星の座標情報インスタンスのリストを取得
        """
        # astropyのTimeタイプへ変換
        timestamp = Time(timestamp)
        # 指定惑星の座標を取得
        planet_coord_list = [
            get_body_barycentric(_planet, timestamp) for _planet in planet_list
        ]

        return planet_coord_list

    _planet_coord_list = _get_planet_coord_list(timestamp, planet_list)

    dict_planet_coord = {}
    for _planet, _coord in zip(planet_list, _planet_coord_list):
        # x, y, z[km]
        x, y, z = _coord.x, _coord.y, _coord.x
        # dict_planet_coord[_planet] = [lon, lat, radius]
        dict_planet_coord[_planet] = {"x": x, "y": y, "z": z}

    return dict_planet_coord


def get_planet_coord_timeseries(timeseries, planet_list):
    """
    指定時系列の指定惑星の座標を取得
    """
    # 初期化
    dict_planet_coord_timeseries = {}
    for _planet in planet_list:
        dict_planet_coord_timeseries[_planet] = {"x": [], "y": [], "z": []}

    # 時系列での各惑星の座標を取得
    for _timestamp in timeseries:
        """
        指定時刻の指定惑星の座標
        key: planet name
        value: dict(x, y, x)
            座標値(km)
        """
        dict_planet_coord = get_planet_coord(_timestamp, planet_list)
        for _planet in planet_list:
            for _key in ["x", "y", "z"]:
                dict_planet_coord_timeseries[_planet][_key].append(
                    np.array(dict_planet_coord[_planet][_key])
                )

    # Convert list into ndarray
    for _planet in planet_list:
        for _key in ["x", "y", "z"]:
            dict_planet_coord_timeseries[_planet][_key] = np.array(
                dict_planet_coord_timeseries[_planet][_key]
            )

    return dict_planet_coord_timeseries


