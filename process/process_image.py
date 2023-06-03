# -*- coding: utf-8 -*-
"""
Created on 03 Jun 2:44 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: calculating night time light index
"""
import pandas as pd
from rasterio.mask import mask


class NLI_recorder:
    """
        多年份多城市的NIL记录器
    """

    def __init__(self):
        self.recorder = pd.DataFrame()

    def add_record(self, new_record):
        self.recorder = pd.concat([self.recorder, new_record])

    @staticmethod
    def gen_record(year, city, NIL):
        return pd.DataFrame({'年份': [year], '地市名称': [city], '灯光指数': [NIL]})

    def release_record(self):
        return self.recorder.sort_values(['年份']).reset_index(drop=True)


def mask_image_with_gdf(image, gdf, nodata=255):
    """
    Args:
        image: 待裁image
        gdf:   裁剪区域
        nodata: 非常重要的一个参数，python中mask后会返回一个外接矩形，nodata用于区分边界内与边界外区域

    Returns:
        mask后的image
    """
    clipped_image, clipped_transform = mask(
        image, gdf.geometry, crop=True, nodata=nodata
    )
    return clipped_image


def cal_NLI(image, light_min=0, light_max=63):
    """NIL计算器，NIL为区域内灯光指数均值

    Args:
        image: 目标image数据
        light_min: 遥感影像内代表灯光最低值的数值
        light_max:遥感影像内代表灯光最大值的数值

    Returns:
        NLI数值
    """
    image_data = image[0]
    NIL = image_data[(image_data >= light_min) & (image_data <= light_max)].mean()
    return NIL
