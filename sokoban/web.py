"""
推箱子后台服务

为什么后台服务是必需的？最开始的想法是“如果有高手解决了一个问题，需要把这个问题的答案记录下来”。这个操作必定需要后端。
"""

import gzip
from os.path import *

from flask import Flask, request, jsonify, Response
from fu import cache
from fu import json
from fu import snow_flake

from sokoban import db, lib

cur = abspath(dirname(__file__))
app = Flask(__name__, static_url_path="/", static_folder=join(cur, '../front/dist'))
# snow用于生成新的ID
snow = snow_flake.SnowFlake()


@app.route("/api/get_maps")
def get_maps():
    content = json.dumps(db.get_all("select * from question order by id"))
    content = gzip.compress(bytes(content, encoding='utf8'))
    return Response(content, headers={
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Encoding": "gzip"
    })


@app.route("/api/submit", methods=['POST'])
def submit():
    """
    提交一个问题，请求中需要包含两个参数：q和a，分别表示question和answer
    :return:服务器想告诉用户的话
    """
    qa = json.loads(request.get_data(as_text=True))
    q = qa['q']
    a = qa['a']
    question = db.get_one("select id,answer from question where question=?", (q,))
    if not question:
        return "没有这个问题"
    a = lib.regularize_operation(a)
    ma = lib.from_xsb_string(q)
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
    cache.clear_cache(db.get_all)
    return "恭喜你创造了奇迹"


@app.route("/api/regularize_map")
def regularize_map():
    s = request.args['map']
    return lib.regularize_xsb_string(s)


@app.route("/api/search_question")
def search_question():
    # 检查有没有类似的问题
    s = request.args['map']
    question = db.get_by_question(s)
    if question:
        return jsonify(question)
    return jsonify(None)


@app.route("/api/add_question")
def add_question():
    # 向题库中添加问题
    s = request.args['map']
    question = db.get_by_question(s)
    if question:
        return "已经有相同的问题了"
    else:
        s = lib.regularize_xsb_string(s)
        ma = lib.from_xsb_string(s)
        # 校验一下问题
        lib.validate(ma)
        q = db.Question(id=snow.get_id(), question=s, answer=None, hard=lib.calculate_hard(ma), hash=None, solve_times=0, extra='')
        db.insert(q)
        cache.clear_cache(db.get_all)
        return "提交问题成功"


if __name__ == '__main__':
    app.run(debug=True, port=5001)
