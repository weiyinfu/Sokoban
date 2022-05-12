from os.path import *
from typing import List

from fu import json
from fu import snow_flake

from sokoban import db
from sokoban import lib, io

cur = dirname(__file__)
ans = json.load(join(cur, 'ans.json'))
maps = io.load_file(join(cur, 'map.txt'))
maps = [i[1] for i in maps]
a: List[db.Question] = []
snow = snow_flake.SnowFlake()
for i in maps:
    q = lib.to_xsb_string(i)
    an = None
    if q in ans:
        an = ans[q]
        del ans[q]
    id = snow.get_id()
    a.append(db.Question(id=id, question=q, answer=an, hard=0, hash="", solve_times=0, extra=""))
assert len(ans) == 0, 'ans中还有新问题'
db.init()
for i in a:
    db.insert(i)
