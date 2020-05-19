from unittest import TestCase
from sokoban import db


class TestDatabase(TestCase):
    def test_validate(self):
        db.validate_data()

    def test_update_hard(self):
        db.update_hard()

    def test_dump(self):
        db.dump("sokoban.json")

    def test_update_map(self):
        db.update_map()

    def test_get_one(self):
        print(db.get_one_by_id('3414290763570315264'))

    def test_get_all(self):
        print(db.get_all())
