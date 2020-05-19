"use strict";
/**
 * webpackConfig过滤器：把webpack配置中的条件语句替换掉
 */
Object.defineProperty(exports, "__esModule", { value: true });
class Item {
    constructor() {
        this.condition = false;
    }
}
exports.Item = Item;
function evaluate(x) {
    if (x.condition === undefined)
        return x;
    return x.condition ? x.ifTrue : x.ifFalse;
}
function evaluateArray(a) {
    return a.map(evaluate).filter((x) => x);
}
function evaluateObject(o) {
    for (let i of Object.keys(o)) {
        if (o[i] instanceof Array) {
            o[i] = evaluateArray(o[i]);
        }
        else if (o[i].condition != undefined) {
            o[i] = evaluate(o[i]);
        }
        else if (typeof o[i] == "object") {
            o[i] = evaluateObject(o[i]);
        }
    }
    return o;
}
function webpackConfigFilter(webpackConfig) {
    return evaluateObject(webpackConfig);
}
exports.default = webpackConfigFilter;
