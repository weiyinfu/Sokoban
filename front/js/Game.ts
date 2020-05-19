//x,y,value三元组，用于记录操作历史
import {BOX, BOX_SLOT, getMan, isOneOf, isOver, legal, loadPsbString, MAN, SLOT, SPACE} from "./lib";

type PositionValue = [number, number, number];

class History {
  /**
   * camera是一个形如[
   * [[x1,y1,v1],[x2,y2,v2]],
   * [[x1,y1,v1],[x1,y1,v1],[x2,y2,v2]],
   * [[x2,y2,v2]]
   * ] 的数组
   *
   * ops是一个操作历史字符串
   * */
  camera: PositionValue[][];
  ops: string[];

  constructor() {
    this.ops = [];
    this.camera = [];
  }


  push(points: number[][], direction: string, curMap: number[][]) {
    this.camera.push(points.map(([x, y]) => [x, y, curMap[x][y]]));
    this.ops.push(direction);
  }


  clear() {
    this.camera = [];
    this.ops = [];
  }


  pop(curMap: number[][]) {
    if (this.camera.length === 0) return;
    this.ops.pop();
    const op = this.camera.pop();
    if (!op) throw new Error("impossible");
    for (let [x, y, value] of op) {
      curMap[x][y] = value;
    }
  }

  peek(): string | null {
    if (this.ops.length === 0) return null;
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
    return this.ops.map(x => x[0]).join("")
  }
}

export class Sokoban {
  curMap: number[][] = [];
  history: History;

  constructor() {
    this.history = new History();
  }

  getLastMove() {
    return this.history.peek() || 'down';
  }


  remove(x: number, y: number, obj: number) {
    //把物体从x，y处移开
    this.curMap[x][y] -= obj;
  }

  put(x: number, y: number, obj: number) {
    this.curMap[x][y] += obj;
  }

  back() {
    this.history.pop(this.curMap);
  }

  loadPsb(psbString: string) {
    this.history.clear();
    this.curMap = loadPsbString(psbString);
  }

  isOver() {
    return isOver(this.curMap);
  }

  getOpList() {
    return this.history.tos();
  }

  move(direction: string): boolean {
    //返回是否移动成功
    const man = getMan(this.curMap);
    const delta = [[0, 1], [0, -1], [1, 0], [-1, 0]]["right left  down up ".split(/\s+/).indexOf(direction)];
    const neibor = [man[0] + delta[0], man[1] + delta[1]];
    const target = [neibor[0] + delta[0], neibor[1] + delta[1]];
    if (!legal(neibor[0], neibor[1], this.curMap)) return false;
    if (isOneOf(this.curMap[neibor[0]][neibor[1]], SPACE, SLOT)) {
      //如果邻居不是物体
      this.history.push([man, neibor], direction, this.curMap);
      this.remove(man[0], man[1], MAN);
      this.put(neibor[0], neibor[1], MAN);
      return true;
    } else if (isOneOf(this.curMap[neibor[0]][neibor[1]], BOX, BOX_SLOT)) {
      //如果邻居是物体
      if (!legal(target[0], target[1], this.curMap)) {
        return false;
      }
      if (isOneOf(this.curMap[target[0]][target[1]], SPACE, SLOT)) {
        this.history.push([man, neibor, target], direction, this.curMap);
        this.remove(neibor[0], neibor[1], BOX);
        this.put(target[0], target[1], BOX);
        this.remove(man[0], man[1], MAN);
        this.put(neibor[0], neibor[1], MAN);
        return true;
      } else {
        return false;
      }
    } else {
      //如果邻居是其它物体
      return false;
    }
  }

}