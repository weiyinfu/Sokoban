export const SPACE = 0,
    SLOT = 1,
    MAN = 2,
    MAN_SLOT = 3,
    BOX = 4,
    BOX_SLOT = 5,
    WALL = 6;
export const PSB_STRING = "-.@+$*#";
export const NAMES = ['space', "slot", 'man', 'man_slot', 'box', 'box_slot', 'wall'];
export type SokobanMap = number[][];

export function loadXsbString(content: string): Array<Array<number>> {
  //直接加载一个地图字符串
  return content.trim().split("\n").filter(line => line.trim().length).map(line => Array.from(line).map(x => PSB_STRING.indexOf(x))
  );
}

export function toXsbString(map: Array<Array<number>>) {
  /**
   * 把一个int数组转成xsb格式的字符串
   * */
  let s: string[] = [];
  for (let i of map) {
    s.push(i.map(x => PSB_STRING[x]).join(''))
  }
  return s.join('\n').trim();
}

export function legal(x: number, y: number, curMap: number[][]) {
  return x >= 0 && y >= 0 && x < curMap.length && y < curMap[x].length;
}

export function isOver(curMap: SokobanMap) {
  //判断游戏是否结束，一个box都没有
  for (let x = 0; x < curMap.length; x++) {
    for (let y = 0; y < curMap[x].length; y++) {
      if (curMap[x] [y] === BOX) {
        return false;
      }
    }
  }
  return true;
}

export function getMan(curMap: SokobanMap) {
  for (let x = 0; x < curMap.length; x++) {
    for (let y = 0; y < curMap[x].length; y++) {
      if (isOneOf(curMap[x][y], MAN, MAN_SLOT)) {
        //如果以man开头，则找到了man
        return [x, y]
      }
    }
  }
  throw new Error("cannot find man");
}

export function isOneOf<T>(v: T, ...options: T[]) {
  return options.indexOf(v) !== -1;
}

export function wrapUrl(url: string) {
  const appName = "/Sokoban/"
  if (url.startsWith("/api/") && location.pathname.startsWith(appName)) {
    url = `${appName}${url.slice(1)}`
  }
  return url;
}