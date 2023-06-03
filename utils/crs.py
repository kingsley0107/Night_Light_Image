# -*- coding: utf-8 -*-
"""
Created on 03 Jun 1:42 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: script for GeoDataframe's crs transform and remote sensing images' crs transform
"""
import os
from functools import lru_cache

import rasterio
from rasterio.crs import CRS
from rasterio.warp import calculate_default_transform, reproject, Resampling

from config.static_vars import PROJ_LIB

os.environ[
    "PROJ_LIB"
] = PROJ_LIB


def gdf_trans_coord(gdf, target_epsg):
    return gdf.to_crs(f"epsg:{target_epsg}")


@lru_cache()
def image_trans_proj(ori_image_path, target_epsg, new_image_path):
    """
    Args:
        ori_image_path: 待投影影像路径
        target_epsg:新投影编码
        new_image_path: 投影后影像文件夹路径

    Returns:
        None, 保存至新路径
    """
    os.makedirs(new_image_path, exist_ok=True)
    ori_image_name = os.path.basename((ori_image_path))
    with rasterio.open(ori_image_path) as ori_image:
        transform, width, height = calculate_default_transform(
            ori_image.crs,
            CRS.from_string(f"EPSG:{target_epsg}"),
            ori_image.width,
            ori_image.height,
            *ori_image.bounds,
        )
        # 创建转换后的影像文件
        output_image_path = new_image_path + "/" + "reproject_" + ori_image_name

        if os.path.exists(output_image_path):
            print(f"{output_image_path} already existed! skip this transfrom !")
            return None
        else:
            print(f"begin transform into {target_epsg}: {output_image_path}")
        with rasterio.open(
                output_image_path,
                "w",
                driver="GTiff",
                width=width,
                height=height,
                count=ori_image.count,
                dtype=ori_image.dtypes[0],
                crs=f"EPSG:{target_epsg}",
                transform=transform,
        ) as dst:
            # 执行影像转换
            reproject(
                source=rasterio.band(ori_image, 1),
                destination=rasterio.band(dst, 1),
                src_transform=ori_image.transform,
                src_crs=ori_image.crs,
                dst_transform=transform,
                dst_crs=f"EPSG:{target_epsg}",
                resampling=Resampling.nearest,
            )
    return None
