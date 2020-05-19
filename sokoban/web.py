"""
一个后台服务，用于记录用户提交的答案
"""

from flask import Flask, request, jsonify
import os
from fu import json
from sokoban import db, lib

cur = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_url_path="/res", static_folder=os.path.join(cur, '../res'))


@app.route("/api/get_index")
def get_index():
    return jsonify(json.load(os.path.join(cur, '../index.json')))


@app.route("/api/get_maps")
def get_maps():
    return jsonify(db.get_all("select * from question order by hard"))


@app.route("/api/submit")
def submit():
    q = request.args['q']
    a = request.args['a']
    question = db.get_one("select id,answer from question where question=?", (q,))
    if not question:
        return "没有这个问题"
    a = lib.regularize_operation(a)
    if not lib.check_right(q, a):
        return "答案根本就不对"
    if len(question.answer) < len(a):
        return "回答正确，但是离最优解还差点"
    if len(question.answer) == len(a):
        return "恭喜你平了世界纪录"
    assert len(question.answer) > len(a)
    db.execute("update question set answer=? where id=?", (a, question.id))
    return "恭喜你创造了奇迹"


if __name__ == '__main__':
    app.run(debug=True)
