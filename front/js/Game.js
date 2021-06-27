"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Game = void 0;
//x,y,value三元组，用于记录操作历史
const lib_1 = require("./lib");
class History {
    constructor() {
        this.ops = [];
        this.camera = [];
    }
    push(points, direction, curMap) {
        this.camera.push(points.map(([x, y]) => [x, y, curMap[x][y]]));
        this.ops.push(direction);
    }
    clear() {
        this.camera = [];
        this.ops = [];
    }
    pop(curMap) {
        if (this.camera.length === 0)
            return;
        this.ops.pop();
        const op = this.camera.pop();
        if (!op)
            throw new Error("impossible");
        for (let [x, y, value] of op) {
            curMap[x][y] = value;
        }
    }
    peek() {
        if (this.ops.length === 0)
            return null;
        return this.ops[this.ops.length - 1];
    }
    size() {
        if (this.ops.length !== this.camera.length) {
            throw new Error("history is disorder");
        }
        return this.ops.length;
    }
    tos() {
        //化为简单字符串
        return this.ops.map(x => x[0]).join("");
    }
}
class Game {
    constructor() {
        this.curMap = [];
        this.question = "";
        this.history = new History();
    }
    getLastMove() {
        return this.history.peek() || 'down';
    }
    remove(x, y, obj) {
        //把物体从x，y处移开
        this.curMap[x][y] -= obj;
    }
    put(x, y, obj) {
        this.curMap[x][y] += obj;
    }
    back() {
        this.history.pop(this.curMap);
    }
    loadXsb(xsbString) {
        this.history.clear();
        this.curMap = lib_1.loadXsbString(xsbString);
        this.question = xsbString;
    }
    isOver() {
        return lib_1.isOver(this.curMap);
    }
    getOpList() {
        return this.history.tos();
    }
    getSize() {
        //获取地图的宽度和高度
        return {
            rows: this.curMap.length,
            cols: this.curMap.reduce((o, n) => o = Math.max(o, n.length), 0)
        };
    }
    move(direction) {
        //返回是否移动成功
        const man = lib_1.getMan(this.curMap);
        const delta = [[0, 1], [0, -1], [1, 0], [-1, 0]]["right left  down up ".split(/\s+/).indexOf(direction)];
        const neibor = [man[0] + delta[0], man[1] + delta[1]];
        const target = [neibor[0] + delta[0], neibor[1] + delta[1]];
        if (!lib_1.legal(neibor[0], neibor[1], this.curMap))
            return false;
        if (lib_1.isOneOf(this.curMap[neibor[0]][neibor[1]], lib_1.SPACE, lib_1.SLOT)) {
            //如果邻居不是物体
            this.history.push([man, neibor], direction, this.curMap);
            this.remove(man[0], man[1], lib_1.MAN);
            this.put(neibor[0], neibor[1], lib_1.MAN);
            return true;
        }
        else if (lib_1.isOneOf(this.curMap[neibor[0]][neibor[1]], lib_1.BOX, lib_1.BOX_SLOT)) {
            //如果邻居是物体
            if (!lib_1.legal(target[0], target[1], this.curMap)) {
                return false;
            }
            if (lib_1.isOneOf(this.curMap[target[0]][target[1]], lib_1.SPACE, lib_1.SLOT)) {
                this.history.push([man, neibor, target], direction, this.curMap);
                this.remove(neibor[0], neibor[1], lib_1.BOX);
                this.put(target[0], target[1], lib_1.BOX);
                this.remove(man[0], man[1], lib_1.MAN);
                this.put(neibor[0], neibor[1], lib_1.MAN);
                return true;
            }
            else {
                return false;
            }
        }
        else {
            //如果邻居是其它物体
            return false;
        }
    }
}
exports.Game = Game;
