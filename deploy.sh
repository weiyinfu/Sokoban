# 上传前端
cd front2
yarn build
cd ..
rsync --progress -r front2/dist me:~/app/Sokoban/front2/
# 上传后端
rsync --progress -r  sokoban me:~/app/Sokoban/

# 上传数据库
rsync --progress -r  sokoban sokoban.db me:~/app/Sokoban/
