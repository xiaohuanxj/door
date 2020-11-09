tag="v`date +"%Y%m%d"`"
docker build --no-cache -t docker.56qq.cn:5000/python3_door_uwsgi_v1:$tag .
docker push docker.56qq.cn:5000/python3_door_uwsgi_v1:$tag
