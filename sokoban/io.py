import os
from typing import List

from sokoban import format

"""
地图IO相关的API
"""


def load_file(filepath: str):
    """
    加载一个文本文件，里面是若干个psb格式的地图
    :param filepath: 加载的文本文件
    :return: 返回（文件描述，llint地图）二元组
    """
    maps = open(filepath).read().strip().split("\n\n")
    maps = [(f"{filepath}", format.from_psb_string(i)) for ind, i in enumerate(maps)]
    return maps


def load_dir(folder: str):
    """
    加载一个目录下的全部地图，每一个文本文件都是一个地图列表
    返回(文件描述,llstr)二元组列表，llstr表示list of list string
    """
    a = []
    for i in os.listdir(folder):
        filepath = os.path.join(folder, i)
        a.extend(load_file(filepath))
    return a


def save_file(filepath: str, a: List[List[List[int]]]):
    """
    把地图a保存到文件filepath中
    """
    s = '\n\n'.join(format.to_psb_string(i) for i in a)
    open(filepath, 'w').write(s)


def save_folder(folder: str, a: List[List[List[int]]]):
    """
    批量保存地图到文件夹folder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    for ind, ma in enumerate(a):
        save_file(os.path.join(folder, f"{ind}.txt"), [ma])
