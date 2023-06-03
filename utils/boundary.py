# -*- coding: utf-8 -*-
"""
Created on 03 Jun 1:49 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: script for city, province gis boundary extraction
"""
from functools import lru_cache

import geopandas as gpd

from config.static_vars import *
from utils.cities import name2code

province_codes = \
    {'新疆维吾尔自治区': 650000,
     '内蒙古自治区': 150000,
     '西藏自治区': 540000,
     '陕西省': 610000,
     '安徽省': 340000,
     '贵州省': 520000,
     '河南省': 410000,
     '辽宁省': 210000,
     '澳门特别行政区': 820000,
     '四川省': 510000,
     '吉林省': 220000,
     '海南省': 460000,
     '甘肃省': 620000,
     '广西壮族自治区': 450000,
     '河北省': 130000,
     '云南省': 530000,
     '北京市': 110000,
     '山东省': 370000,
     '湖南省': 430000,
     '江苏省': 320000,
     '广东省': 440000,
     '黑龙江省': 230000,
     '山西省': 140000,
     '湖北省': 420000,
     '福建省': 350000,
     '江西省': 360000,
     '宁夏回族自治区': 640000,
     '青海省': 630000,
     '浙江省': 330000,
     '上海市': 310000,
     '台湾省': 710000,
     '天津市': 120000,
     '香港特别行政区': 810000,
     '重庆市': 500000}


# 缓存器,妈妈再也不用担心多次调用浪费时间
@lru_cache()
def get_all_cities():
    all_cities = gpd.read_file(ALL_CITIES_DATA_PATH)
    return all_cities


def province_name2code(province_name):
    return province_codes[province_name]


def extract_province_boundary(province_adcode=440000):
    """按照省级别提取边界，内部是一个个城市

    Args:
        province_adcode (_type_, optional): _省行政编码_. Defaults to 440000.

    Returns:
        _type_: 由城市为单元组成的省级矢量数据
    """
    all_cities = get_all_cities()
    target_province = all_cities[all_cities["省级码"] == int(province_adcode)][
        ["地名", "地级码", "地级类", "省级", "省级码", "geometry"]
    ]
    target_province.columns = [
        "city_name",
        "adcode",
        "class",
        "province_name",
        "province_adcode",
        "geometry",
    ]
    return target_province.reset_index(drop=True)


def extract_city_boundary(city_adcode=name2code("广州")):
    """按照城市级别提取边界

    Args:

        city_adcode (_type_, optional): _城市行政编码_. Defaults to name2code("广州").

    Returns:
        _type_: _description_
    """
    all_cities = get_all_cities()
    target_city = all_cities[all_cities["地级码"] == int(city_adcode)][
        ["地名", "地级码", "地级类", "省级", "省级码", "geometry"]
    ]
    target_city.columns = [
        "city_name",
        "adcode",
        "class",
        "province_name",
        "province_adcode",
        "geometry",
    ]
    return target_city.reset_index(drop=True)
