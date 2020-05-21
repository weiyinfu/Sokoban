cd front
webpack
cd ..
rsync --progress -r  sokoban sokoban.db tencent:/home/ubuntu/app/Sokoban/
rsync --progress -r front/dist tencent:/home/ubuntu/app/Sokoban/front/
