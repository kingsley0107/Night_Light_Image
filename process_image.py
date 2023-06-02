# -*- coding: utf-8 -*-
"""
Created on 02 Jun 3:12 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_:
"""
import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.crs import CRS
from rasterio.mask import mask
import geopandas as gpd


def batch_reproject_images(origin_file_path, reprojected_file_path, target_epsg):
    os.environ['PROJ_LIB'] = r'C:\Users\20191\anaconda3\Lib\site-packages\pyproj\proj_dir\share\proj'
    os.makedirs(reprojected_file_path, exist_ok=True)
    path, _, origin_images = list(os.walk(origin_file_path))[0]
    for yearly_image in origin_images:
        with rasterio.open(path + yearly_image) as image:
            # 计算原始影像到目标坐标系的转换参数
            transform, width, height = calculate_default_transform(image.crs, CRS.from_string(f'EPSG:{target_epsg}'),
                                                                   image.width,
                                                                   image.height, *image.bounds)

            # 创建转换后的影像文件
            output_file = reprojected_file_path + "reproject_" + yearly_image
            with rasterio.open(output_file, 'w', driver='GTiff', width=width, height=height, count=image.count,
                               dtype=image.dtypes[0], crs=f'EPSG:{target_epsg}', transform=transform) as dst:
                # 执行影像转换
                reproject(
                    source=rasterio.band(image, 1),
                    destination=rasterio.band(dst, 1),
                    src_transform=image.transform,
                    src_crs=image.crs,
                    dst_transform=transform,
                    dst_crs=f'EPSG:{target_epsg}',
                    resampling=Resampling.nearest
                )

def clip_image_by_boundary(boundary,image):
    pass

if __name__ == "__main__":
    origin_file_path = r"./night_images/"
    reprojected_file_path = r"./night_images_reproject/"
    target_epsg = 3857
    # batch_reproject_images(origin_file_path=origin_file_path, reprojected_file_path=reprojected_file_path,
    #                        target_epsg=target_epsg)
    gdf = gpd.read_file(r'./boundary/guangdong_proj.geojson')
    path,_,name = list(os.walk(reprojected_file_path))[0]
