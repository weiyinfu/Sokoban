from os.path import *
from typing import List
from unittest import TestCase

from sokoban import db
from sokoban import lib
from sokoban.db import Question


class TestDatabase(TestCase):
    def test_validate(self):
        db.validate_data()

    def test_update_hard(self):
        db.update_hard()

    def test_dump(self):
        filepath = join(dirname(__file__), '../sokoban.json')
        db.dump(filepath)

    def test_update_map(self):
        db.update_map()

    def test_get_one(self):
        print(db.get_one('select * from question where id=3414290763570315264'))

    def test_get_all(self):
        print(db.get_all())

    def test_map_regularize(self):
        """
        检测数据库中地图是否正则化
        :return:
        """
        a: List[Question] = db.get_all()
        for i in a:
            q = lib.regularize_xsb_string(i.question)
            if q != i.question:
                print(i.question)
                print('-------')
                print(q)
