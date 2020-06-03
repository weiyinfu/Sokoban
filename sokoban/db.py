import os
from typing import List, Iterable

from fu import cache
from fu import json
from fu import sqlite_util as d
from tqdm import tqdm

from sokoban import lib

db_path = os.path.join(os.path.dirname(__file__), '../sokoban.db')
conn = d.get_conn(db_path)


def init():
    """
    初始化数据库
    :return:
    """
    if not d.exist_table(conn, 'question'):
        d.init_structure(conn, """
        create table question(
        id varchar(50) primary key not NULL,-- 主键
        question text unique not NULL, -- 地图
        answer text,  -- 最佳答案
        hard int,-- 问题的难度
        hash varchar(128),-- 地图的key
        extra text,-- json格式的extra
        solve_times int); -- 问题被解决的次数
        """)


class Question:
    """
    问题类，一个问题包括以下字段
    """

    def __init__(self, id: int, question: str, answer: str, hard: int, hash: str, solve_times: int, extra: str):
        self.id = id
        self.question = question
        self.answer = answer
        self.hard = hard
        self.hash = hash
        self.solve_times = solve_times  # 问题被解决的次数，表示了问题的受欢迎程度
        self.extra = extra


def insert(q: Question):
    # 向数据库中插入一条数据
    return d.insert_one(conn, 'question', q,
                        ['id', 'question', 'answer', 'hard', 'hash', 'solve_times', 'extra'])


@cache.simple_cache()
def get_all(sql="select * from question") -> List[Question]:
    """
    获取全部数据
    :return:
    """
    return d.select_list(conn, sql)


def get_list(sql, args: Iterable) -> List[Question]:
    return d.select_list(conn, sql, args)


def get_one(sql, args: Iterable = tuple()) -> Question:
    return d.select_list(conn, sql, args)[0]


def dump(filepath: str):
    json.dump(get_all(), filepath)


def execute(sql: str, args: Iterable = tuple()):
    conn.execute(sql, args)
    conn.commit()


def update_map():
    """
    更新数据库中的地图，在更新地图的同时，必须更新答案
    这个操作很危险，在执行之前必须做好数据库备份
    :return:
    """
    a: List[Question] = d.select_list(conn, "select id,question,answer from question")
    for q in tqdm(a, desc="update_map"):
        ma = lib.from_xsb_string(q.question)
        answer = lib.regularize_operation(q.answer) if q.answer else q.answer
        reg_ma = lib.regularize(ma)
        xsb_string = lib.to_xsb_string(reg_ma)
        if xsb_string != q.question or answer != q.answer:
            print("need format")
            if xsb_string != q.question and answer:
                """
                如果地图被规范化了，那么答案也必须规范化
                """
                answer = lib.try_op(ma, answer)
            conn.execute("update question set question=?,answer=? where id=?", (xsb_string, answer, q.id,))
    conn.commit()


def update_hard():
    """
    使用hard评估函数更新难度
    :return:
    """
    a: List[Question] = d.select_list(conn, "select id,question from question")
    for q in tqdm(a, desc='update_hard'):
        ma = lib.from_xsb_string(q.question)
        hard = lib.calculate_hard(ma)
        conn.execute("update question set hard=? where id=?", (hard, q.id))
    conn.commit()


def validate_data():
    """
    调用validate函数检查数据库中的每一个问题
    :return:
    """
    a: List[Question] = d.select_list(conn, "select id,question,answer from question")
    for q in a:
        ma = lib.from_xsb_string(q.question)
        try:
            lib.validate(ma)
        except Exception as e:
            print('地图不合法', e)
            print(ma)
            print(q.question)
            assert False
        an = q.answer
        if an:
            assert lib.check_right(ma, an)


def get_by_id(question_id: int):
    return get_one('select * from question where id=?', (question_id,))


def get_by_question(xsb_str: str):
    xsb_str = lib.regularize_xsb_string(xsb_str)
    question_list = get_list("select * from question where question=?", (xsb_str,))
    assert question_list.__len__() <= 1, '问题描述应该是唯一的'
    return None if len(question_list) == 0 else question_list[0]
