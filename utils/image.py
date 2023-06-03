# -*- coding: utf-8 -*-
"""
Created on 03 Jun 2:56 PM

@Author: kingsley leung
@Email: kingsleyl0107@gmail.com

_description_: simple script for simple image processing
"""

from functools import lru_cache
import rasterio


@lru_cache(maxsize=128)
def image_reader(image_path):
    image = rasterio.open(image_path)
    return image
