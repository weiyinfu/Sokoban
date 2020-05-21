from typing import List, Iterable
from functools import lru_cache
from fu import json
from fu import sqlite_util as d
from tqdm import tqdm
from fu import cache
from sokoban import lib
import os

db_path = os.path.join(os.path.dirname(__file__), '../sokoban.db')
conn = d.get_conn(db_path)


def init(force: bool = False):
    if force or not d.exist_table(conn, 'question'):
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
    def __init__(self, id, question: str, answer: str, hard: int, hash: str, solve_times: int):
        self.id = id
        self.question = question
        self.answer = answer
        self.hard = hard
        self.hash = hash
        self.solve_times = solve_times


def insert(q: Question):
    return d.insert_one(conn, 'question', q, ['id', 'question', 'answer', 'hard', 'hash', 'solve_times'])


@cache.simple_cache()
def get_all(sql="select * from question") -> List[Question]:
    """
    获取全部数据
    :return:
    """
    return d.select_json(conn, sql)


def get_one_by_id(question_id: str) -> Question:
    """
    获取一个答案
    :return:
    """
    li = d.select_obj(conn, "select * from question where id=?", (question_id,))
    assert len(li) == 1
    return li[0]


def get_list(sql, args: Iterable) -> List[Question]:
    li = d.select_obj(conn, sql, args)
    return li


def get_one(sql, args: Iterable) -> Question:
    li = get_list(sql, args)
    assert len(li) == 1
    return li[0]


def dump(filepath: str):
    json.dump(get_all(), filepath)


def execute(sql: str, args: Iterable):
    conn.execute(sql, args)
    conn.commit()


def update_map():
    """
    更新数据库中的地图，在更新地图的同时，必须更新答案
    :return:
    """
    a: List[Question] = d.select_obj(conn, "select id,question,answer from question")
    for q in tqdm(a, desc="update_map"):
        ma = lib.from_psb_string(q.question)
        answer = lib.regularize_operation(q.answer) if q.answer else q.answer
        reg_ma = lib.regularize(ma, True)
        psb_string = lib.to_psb_string(reg_ma)
        if psb_string != q.question or answer != q.answer:
            print("need format")
            if psb_string != q.question and answer:
                """
                如果地图被规范化了，那么答案也必须规范化
                """
                answer = lib.try_op(ma, answer)
            conn.execute("update question set question=?,answer=? where id=?", (psb_string, answer, q.id,))
    conn.commit()


def update_hard():
    """
    更新难度
    :return:
    """
    a: List[Question] = d.select_obj(conn, "select id,question from question")
    for q in tqdm(a, desc='update_hard'):
        ma = lib.from_psb_string(q.question)
        hard = lib.hard(ma)
        conn.execute("update question set hard=? where id=?", (hard, q.id))
    conn.commit()


def validate_data():
    """
    调用validate函数
    :return:
    """
    a: List[Question] = d.select_obj(conn, "select id,question,answer from question")
    for q in a:
        ma = lib.from_psb_string(q.question)
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
