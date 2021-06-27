from sokoban import db

a = db.get_all()
print(len(a))
import json
import msgpack

s = json.dumps(a)
b = bytes(s, encoding='utf8')
import math

print(len(b))


def human_size(sz: int):
    # 把一个文件大小转成可读性较好的字符串
    s = 'BkMG'
    x = math.floor(math.log(sz, 1024))
    num = sz / 1024 ** x
    return f"{num:.2f}{s[int(x)]}"


print(human_size(len(b)))
resp = msgpack.dumps(a)
print(len(resp), human_size(len(resp)))
import zstd

z = zstd.ZstdCompressor(zstd.MAX_COMPRESSION_LEVEL)
compressed = z.compress(resp)
print(len(compressed), human_size(len(compressed)))
import gzip

compressed2 = gzip.compress(resp)
print(human_size(len(compressed2)))
