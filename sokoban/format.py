from typing import List, Dict
import copy
import re

"""
地图格式相关的API
"""


def to_psb(a: List[List[int]], ground='-'):
    """
    把一个地图转化为psb格式
    因为ground有争议，此处使用-
    """
    chars = [ground] + list(".@+$*#")
    ids = [i for i in range(len(chars))]
    return transform(a, dict(zip(ids, chars)))


def from_psb_string(a: str):
    lines = a.strip().splitlines()
    valid_lines = []
    meet_end = False
    for line in lines:
        is_line = re.match("^[.@+$*#_\\-]", line)
        if is_line:
            if meet_end:
                print(a)
                raise Exception("已经解析完毕了又遇到了新行")
            else:
                valid_lines.append(line)
        else:
            meet_end = True
    valid_lines = [list(line.replace('_', '-').strip()) for line in valid_lines if line.strip()]
    return to_llint(valid_lines)


def to_psb_string(a: List[List[int]]):
    """
    把一个地图转化为一个字符串，形如
    123434
    123434
    234345
    """
    a = to_psb(a)
    return '\n'.join(''.join(map(str, row)) for row in a)


def transform(a: List[List[str]], ma: Dict[str, str]):
    """
    a是一个llint格式的地图，把它用ma进行映射
    """
    b = []
    for row in a:
        line = []
        for col, v in enumerate(row):
            line.append(ma[v])
        b.append(line)
    return b


def to_llint(a: List[List[int]]):
    chars = list("-.@+$*#")
    return transform(a, dict(zip(chars, range(len(chars)))))
