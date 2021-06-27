import os
from sokoban import lib, io

from fu import json

qa = json.load("../ans.json")
for k,v in qa.items():
    assert lib.check_right(lib.from_xsb_string(k),v)
a = [lib.from_xsb_string(i) for i in qa]
print('去重之前', len(a))
for ma in a:
    lib.validate(ma)
valid = lib.dedup(list(range(len(a))), a)
print('去重之后', len(valid))

ans_map = {}
for i in qa:
    k = lib.to_xsb_string(lib.regularize(lib.from_xsb_string(i)))
    v = lib.try_op(lib.from_xsb_string(k), qa[i])
    if not v:
        assert False
    if k in ans_map:
        if len(v) > len(ans_map[k]):
            continue
    ans_map[k] = v
for k, v in ans_map.items():
    assert lib.check_right(lib.from_xsb_string(k), v)
json.dump(ans_map, 'new_ans.json', indent=2)
print(len(ans_map))
