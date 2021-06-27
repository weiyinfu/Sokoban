import os
from sokoban import lib, io

a = io.load_dir("../maps")
print('去重之前', len(a))
for filepath, ma in a:
    lib.validate(ma)
filenames = [i[0] for i in a]
maps = [i[1] for i in a]
valid=lib.dedup(filenames, maps)
print('去重之后',len(valid))
open('map.txt','w').write("\n\n".join(lib.to_xsb_string(i) for i in valid))