import re
from collections import Counter
from typing import List, Dict, Any, Union

import numpy as np

"""
标准的地图应该是一个二维llint列表，llint
"""

images = ["space", 'slot', "man", "manSlot", 'box', 'boxSlot', "wall"]
SPACE, SLOT, MAN, MAN_SLOT, BOX, BOX_SLOT, WALL = list(range(len(images)))


def to_xsb_string(a: Union[List[List[int]], np.ndarray], ground='-'):
    """
    把一个地图转化为xsb格式
    因为ground有争议，此处使用-
    """
    chars = [ground] + list(".@+$*#")
    ids = [i for i in range(len(chars))]
    a = transform(a, dict(zip(ids, chars)))
    return '\n'.join(''.join(map(str, row)) for row in a)


def from_xsb_string(a: str):
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
    chars = list("-.@+$*#")
    return transform(valid_lines, dict(zip(chars, range(len(chars)))))


def transform(a: List[List[Any]], ma: Dict[Any, str]):
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


def pad(ma: List[List[int]]):
    """
    把一个地图用墙围起来，求出最大行列，然后用空白填充
    :param ma:
    :return:
    """
    rows, cols = len(ma), max(len(i) for i in ma)
    ans = [[WALL] * (cols + 2)]
    for i in ma:
        ans.append([WALL] + i + [WALL] * (cols + 2 - 1 - len(i)))
    ans.append([WALL] * (cols + 2))
    return ans


def regularize_xsb_string(s: str):
    ma = from_xsb_string(s)
    ma = regularize(ma)
    return to_xsb_string(ma)


def regularize(ma: List[List[Any]]):
    """
    规范化一个地图
    计算一个地图的哈希值，将一个地图顺时针旋转4次，flip之后再旋转4次，一共得到8种局面，取这8种局面中的最小局面作为局面的正则化值
    """
    ma = pad(ma)
    ma = strip(ma)
    # 开始旋转计算最小值
    min_str = None
    best_map = None
    for a in (np.array(ma), np.flip(ma)):
        now = a
        for i in range(4):
            now = np.rot90(now)
            h = to_xsb_string(now)
            if not min_str or min_str > h:
                min_str = h
                best_map = now
    return best_map


def get_man_pos(ma: List[List[int]]):
    """
    获取地图中人的位置
    """
    for x in range(len(ma)):
        for y in range(len(ma[x])):
            v = ma[x][y]
            if v == MAN or v == MAN_SLOT:
                return x, y
    print(to_xsb_string(ma))
    assert False, "cannot find man"


def show(a: List[List[Any]]):
    """
    打印一个地图
    """
    print(to_xsb_string(a))
    print('\n')


def strip(ma: List[List[int]]):
    """
    strip一个地图：去掉地图中人不可能到达的部分，只保留最小的那一部分地图。
    使用搜索的方式寻找人所能到达的全部位置
    """
    visited = np.zeros_like(ma, dtype=np.bool)
    man_pos = get_man_pos(ma)
    q = [man_pos]
    visited[man_pos[0], man_pos[1]] = True
    valid_wall = set()
    while q:
        x, y = q.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            xx, yy = x + dx, y + dy
            if not (len(ma) > xx >= 0 and len(ma[xx]) > yy >= 0):
                # 直接跑出去了，说明地图少”墙“
                print(ma)
                assert False, "no wall"
            if ma[xx][yy] != WALL:
                if not visited[xx][yy]:
                    visited[xx][yy] = True
                    q.append((xx, yy))
            else:
                valid_wall.add((xx, yy))
    # 只保留有效的墙，给墙瘦身
    for x in range(len(ma)):
        for y in range(len(ma[x])):
            if ma[x][y] == WALL:
                # 未到之墙等于空白
                if (x, y) not in valid_wall:
                    ma[x][y] = 0
    # 截取片段
    rec = [1e9, -1, 1e9, -1]
    for x in range(len(ma)):
        for y in range(len(ma[x])):
            if visited[x, y]:
                rec[0] = min(x, rec[0])
                rec[1] = max(x, rec[1])
                rec[2] = min(y, rec[2])
                rec[3] = max(y, rec[3])
    ma = np.array(ma)[rec[0] - 1:rec[1] + 2, rec[2] - 1:rec[3] + 2]
    return ma


def validate(ma: List[List[int]]):
    """
    校验一个地图的合法性
    1. 有界性
    2. 目标位置与箱子的个数
    3. 有解性如何判定？
    """
    # strip保证了有界性
    ma = regularize(ma)
    # 目标位置的个数与箱子的个数
    a = np.reshape(ma, -1).tolist()
    cnt = Counter(a)
    slot_count = cnt[MAN_SLOT] + cnt[SLOT]
    box_count = cnt[BOX]
    if slot_count < box_count:
        show(ma)
        print(cnt)
        print("slot个数", slot_count, "箱子个数", box_count)
        raise Exception("slot与箱子个数不一致")
    if is_over(a):
        raise Exception("此游戏已经处于结束状态了")


def dedup(filenames: List[str], maps: List[List[List[int]]]):
    """
    消重，去掉重复的地图。
    方法：把地图进行正则化，把地图弄成最规范的地图，然后比较地图
    """
    s = {}
    good = []
    for mapIndex, ma in enumerate(maps):
        ma = regularize(ma)
        k = to_xsb_string(ma)
        if k in s:
            print(filenames[s[k]], filenames[mapIndex])
            print("duplicate")
            show(ma)
            show(maps[s[k]])
            continue
        s[k] = mapIndex
        good.append(ma)
    return good


def calculate_hard(regular_map: List[List[int]]) -> float:
    """
    评价一个局面的难易程度
    :return: 返回一个浮点数表示难易程度
    """
    regular_map = np.array(regular_map)
    cnt = Counter(np.reshape(regular_map, -1))
    return cnt[SLOT] + regular_map.shape[0] * regular_map.shape[1]


def is_over(a: List[List[int]]):
    """
    检验一个状态是否是结束状态
    """
    return Counter(np.reshape(a, -1))[BOX] == 0


def regularize_operation(opList: str):
    for o, n in zip("上下左右", 'udlr'):
        opList = opList.replace(o, n)
    opList = re.sub("[^udlr]", "", opList.lower())
    return opList


def eight_op(opList: str):
    # 把一个oplist变成8种操作序列，对应8种变换
    opList = regularize_operation(opList)
    udlr = 'urdl'
    drul = 'uldr'

    def make_map(k, v):
        return dict(zip(k, v))

    ops = []
    for i in (udlr, drul):
        for turn in range(4):
            op_map = make_map(i, [udlr[(turn + ind) % 4] for ind in range(4)])
            new_opList = [op_map[op] for op in opList]
            ops.append(''.join(new_opList))
    return ops


def try_op(a: List[List[int]], opList: str):
    """
    正则化的时候需要考虑答案一起正则化
     对oplist执行8种变换，判断是否能够解决问题，如果可以，返回opList，否则，返回空
    :param a:
    :param opList:
    :return:
    """
    for eight in eight_op(opList):
        if check_right(a, eight):
            return eight


def check_right(a: List[List[int]], opList: str):
    """
    检验一个操作系列是否能够解决a问题,opList是一个包含u,d,l,r四种操作的字符串，形如：uuddllr
    """
    a = np.array(a)
    opList = regularize_operation(opList)

    def legal(x, y):
        return len(a) > x >= 0 and len(a[x]) > y >= 0

    def remove(x, y, obj):
        a[x, y] -= obj

    def put(x, y, obj):
        a[x, y] += obj

    for op in opList:
        if op not in "udlr": raise Exception(f"cannot find operation with name:^{op}$")
        dx, dy = ((-1, 0), (1, 0), (0, -1), (0, 1))["udlr".index(op)]
        man = get_man_pos(a)
        neibor = (man[0] + dx, man[1] + dy)
        target = (neibor[0] + dx, neibor[1] + dy)
        if not legal(neibor[0], neibor[1]):
            return False
        if a[neibor[0], neibor[1]] in (SPACE, SLOT):
            # neibor是空白，没有推任何东西
            remove(man[0], man[1], MAN)
            put(neibor[0], neibor[1], MAN)
        elif a[neibor[0], neibor[1]] in (BOX, BOX_SLOT):
            # neibor不是空白，正在推箱子
            if not legal(*target):
                return False
            if a[target[0], target[1]] in (SPACE, SLOT):
                # 如果推动箱子的目的地是空白，那么可以推动
                remove(man[0], man[1], MAN)
                remove(neibor[0], neibor[1], BOX)
                put(neibor[0], neibor[1], MAN)
                put(target[0], target[1], BOX)
            else:
                # 推动箱子的目的地不是空白，推不动
                return False
        else:
            return False
    if is_over(a):
        return True
    else:
        return False


def argsort_by_hard(maps: List[List[List[int]]]):
    """
    将地图按照难易程度进行排序
    """
    hard_list = []
    for a in maps:
        hard_list.append(calculate_hard(a))
    return np.argsort(hard_list)
