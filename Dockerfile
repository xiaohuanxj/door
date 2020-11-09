FROM docker.56qq.com/python3_door_base:v20180815 
MAINTAINER Liqiao.liu <liqiao.liu@56qq.com>
ADD requirements.txt /requirements.txt
ADD pip.conf /root/.pip/pip.conf
# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

# Time Zone
RUN echo "Asia/Shanghai" > /etc/timezone
#RUN dpkg-reconfigure -f noninteractive tzdata

ADD . /door/

WORKDIR /door

EXPOSE 8080
CMD /usr/local/bin/uwsgi --ini uwsgi.ini && tail -f /door/logs/all.log

