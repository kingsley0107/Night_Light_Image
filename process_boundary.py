# -*- coding: utf-8 -*-
"""
Created on 02 Jun 3:03 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_:
"""
import geopandas as gpd
import os

def extract_boundary(cn_city_level_gdf,province_code=440000):
    target_province = cn_city_level_gdf[cn_city_level_gdf["省级码"] == province_code][["地名", "地级码", "地级类", "省级", "省级码", "geometry"]]
    target_province.columns = [
        "city_name",
        "adcode",
        "class",
        "province_name",
        "province_adcode",
        "geometry",
    ]
    return target_province

def trans_crs(origin_gdf,target_crs):
    return origin_gdf.to_crs(f"epsg:{target_crs}")

if __name__ == "__main__":
    all_cities = gpd.read_file(r"./地市边界/地级.shp")
    os.makedirs(r'./boundary', exist_ok=True)
    guangdong_proj = trans_crs(extract_boundary(all_cities, province_code=440000),3857)
    guangdong_proj.to_file(r"./boundary/guangdong_proj.geojson")