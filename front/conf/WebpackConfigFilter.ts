/**
 * webpackConfig过滤器：把webpack配置中的条件语句替换掉
 */

export class Item {
    condition: boolean | (() => boolean) = false;
    ifTrue: any;
    ifFalse?: any;
}

function evaluate(x: Item | any): any {
    if (x.condition === undefined) return x;
    return x.condition ? x.ifTrue : x.ifFalse;
}

function evaluateArray(a: Item[] | any): any {
    return a.map(evaluate).filter((x: any) => x);
}

function evaluateObject(o: any) {
    for (let i of Object.keys(o)) {
        if (o[i] instanceof Array) {
            o[i] = evaluateArray(o[i])
        } else if (o[i].condition != undefined) {
            o[i] = evaluate(o[i])
        } else if (typeof o[i] == "object") {
            o[i] = evaluateObject(o[i])
        }
    }
    return o
}

export default function webpackConfigFilter(webpackConfig: any) {
    return evaluateObject(webpackConfig)
}
