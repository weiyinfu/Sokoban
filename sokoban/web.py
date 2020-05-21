"""
一个后台服务，用于记录用户提交的答案
"""

from flask import Flask, request, jsonify
import os
from fu import json
from sokoban import db, lib
from os.path import *
from fu import cache

cur = abspath(dirname(__file__))
app = Flask(__name__, static_url_path="/", static_folder=join(cur, 'front/dist'))


@app.route("/api/get_index")
def get_index():
    return jsonify(json.load(os.path.join(cur, '../index.json')))


@app.route("/api/get_maps")
def get_maps():
    return jsonify(db.get_all("select * from question order by hard"))


@app.route("/api/submit")
def submit():
    """
    提交一个问题
    :return:
    """
    q = request.args['q']
    a = request.args['a']
    question = db.get_one("select id,answer from question where question=?", (q,))
    if not question:
        return "没有这个问题"
    a = lib.regularize_operation(a)
    ma = lib.from_psb_string(q)
    if not lib.check_right(ma, a):
        return "答案根本就不对"
    if question.answer:
        if len(question.answer) < len(a):
            return f"回答正确，但是{len(a)}离最优解{len(question.answer)}还差点。"
        if len(question.answer) == len(a):
            return "恭喜你平了世界纪录"
        assert len(question.answer) > len(a)
    db.execute("update question set answer=? where id=?", (a, question.id))
    # 因为有新答案来了，所以需要清空缓存
    cache.clear_cache()
    return "恭喜你创造了奇迹"


if __name__ == '__main__':
    app.run(debug=True)
