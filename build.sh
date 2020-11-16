tag="v`date +"%Y%m%d"`"
docker build --no-cache -t docker.xxx.cn:5000/python3_door_uwsgi_v1:$tag .
docker push docker.xxx.cn:5000/python3_door_uwsgi_v1:$tag
