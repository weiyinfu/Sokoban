import os
from os.path import *

from fu import json

from sokoban import lib

"""
生成资源索引：Java也需要使用此索引
"""
cur = dirname(__file__)
skins = []
skin_folder = join(cur, "skin")
for skin in os.listdir(skin_folder):
    dirname = join(skin_folder, skin)
    ma = {}
    for i in os.listdir(dirname):
        name = splitext(i)[0]
        ma[name] = os.path.relpath(join(dirname, i), cur)
        if name == "man":
            # 如果没有四个方向，那么使用man代替
            ma['up'] = ma['down'] = ma['left'] = ma['right'] = ma[name]
    skins.append({'name': skin, "images": ma})

json.dump({
    'skins': skins,
    # 地图中数字跟images的映射
    "images": lib.images
}, "front/static/index.json", ensure_ascii=0, indent=2)
