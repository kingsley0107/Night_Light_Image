# -*- coding: utf-8 -*-
"""
Created on 03 Jun 2:12 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: static variables in this project
"""
import os

ALL_CITIES_DATA_PATH = r"./地市边界/地级.shp"
RAW_NIGHT_IMAGES_FOLDER_PATH = r"./night_images"
PROJECTED_NIGHT_IMAGES_FOLDER_PATH = r"./night_images_reproject"

RESULT_PATH = r"./result/result.csv"
os.makedirs(os.path.dirname(RESULT_PATH), exist_ok=True)
PROGRAM_PROJECT_UNICODE = 3857
PROGRAM_GEO_UNCIODE = 4326

# PROJ库绝对路径，不设置会导致EPSG编码搜索报错
PROJ_LIB = r"C:\Users\20191\anaconda3\Lib\site-packages\pyproj\proj_dir\share\proj"

target_cities = ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市',
                 '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '中山市', '潮州市', '揭阳市', '云浮市']
