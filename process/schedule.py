# -*- coding: utf-8 -*-
"""
Created on 03 Jun 3:12 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: schedule for the project
"""

import os

from tqdm import tqdm

from config.static_vars import target_cities, RAW_NIGHT_IMAGES_FOLDER_PATH, PROJECTED_NIGHT_IMAGES_FOLDER_PATH, \
    PROGRAM_PROJECT_UNICODE
from process.process_image import mask_image_with_gdf, NLI_recorder, cal_NLI
from utils.boundary import extract_city_boundary
from utils.cities import name2code
from utils.crs import gdf_trans_coord, image_trans_proj
from utils.image import image_reader


def schedule():
    recorder = NLI_recorder()
    for city in tqdm(target_cities):
        # 确保所有数据转换为同一投影坐标
        city_boundary_proj = gdf_trans_coord(extract_city_boundary(name2code(city)), PROGRAM_PROJECT_UNICODE)
        # 自动处理所有年份遥感数据
        raw_img_path, _, image_names = list(os.walk(RAW_NIGHT_IMAGES_FOLDER_PATH))[0]
        for image_in_year in image_names:
            image_trans_proj(raw_img_path + '/' + image_in_year, PROGRAM_PROJECT_UNICODE,
                             PROJECTED_NIGHT_IMAGES_FOLDER_PATH)
            proj_img = image_reader(PROJECTED_NIGHT_IMAGES_FOLDER_PATH + "/reproject_" + image_in_year)
            # 以城市为边界进行mask
            clipped_image = mask_image_with_gdf(proj_img, city_boundary_proj, 255)

            # 插入recorder
            _this_NIL = cal_NLI(clipped_image, 0, 63)
            _this_year = image_in_year.replace(".tif", "")[-4:]
            new_record = NLI_recorder.gen_record(_this_year, city, _this_NIL)
            recorder.add_record(new_record)
    return recorder.release_record()


if __name__ == "__main__":
    result = schedule()
