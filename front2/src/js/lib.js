"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.wrapUrl = exports.isOneOf = exports.getMan = exports.isOver = exports.legal = exports.toXsbString = exports.loadXsbString = exports.NAMES = exports.PSB_STRING = exports.WALL = exports.BOX_SLOT = exports.BOX = exports.MAN_SLOT = exports.MAN = exports.SLOT = exports.SPACE = void 0;
exports.SPACE = 0, exports.SLOT = 1, exports.MAN = 2, exports.MAN_SLOT = 3, exports.BOX = 4, exports.BOX_SLOT = 5, exports.WALL = 6;
exports.PSB_STRING = "-.@+$*#";
exports.NAMES = ['space', "slot", 'man', 'man_slot', 'box', 'box_slot', 'wall'];
function loadXsbString(content) {
    //直接加载一个地图字符串
    return content.trim().split("\n").filter(line => line.trim().length).map(line => Array.from(line).map(x => exports.PSB_STRING.indexOf(x)));
}
exports.loadXsbString = loadXsbString;
function toXsbString(map) {
    /**
     * 把一个int数组转成xsb格式的字符串
     * */
    let s = [];
    for (let i of map) {
        s.push(i.map(x => exports.PSB_STRING[x]).join(''));
    }
    return s.join('\n').trim();
}
exports.toXsbString = toXsbString;
function legal(x, y, curMap) {
    return x >= 0 && y >= 0 && x < curMap.length && y < curMap[x].length;
}
exports.legal = legal;
function isOver(curMap) {
    //判断游戏是否结束，一个box都没有
    for (let x = 0; x < curMap.length; x++) {
        for (let y = 0; y < curMap[x].length; y++) {
            if (curMap[x][y] === exports.BOX) {
                return false;
            }
        }
    }
    return true;
}
exports.isOver = isOver;
function getMan(curMap) {
    for (let x = 0; x < curMap.length; x++) {
        for (let y = 0; y < curMap[x].length; y++) {
            if (isOneOf(curMap[x][y], exports.MAN, exports.MAN_SLOT)) {
                //如果以man开头，则找到了man
                return [x, y];
            }
        }
    }
    throw new Error("cannot find man");
}
exports.getMan = getMan;
function isOneOf(v, ...options) {
    return options.indexOf(v) !== -1;
}
exports.isOneOf = isOneOf;
function wrapUrl(url) {
    const appName = "/Sokoban/";
    if (url.startsWith("/api/") && location.pathname.startsWith(appName)) {
        url = `${appName}${url.slice(1)}`;
    }
    return url;
}
exports.wrapUrl = wrapUrl;
