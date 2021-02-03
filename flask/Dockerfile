FROM local/centos7
RUN yum -y update;yum -y install epel-release;yum -y install python36
ENV FLASK_APP index.py
ENV FLASK_DEBUG 1
ENV FLASK_CONFIG docker
ENV ENV DEV
ENV DB_HOST 172.18.0.110
ENV DB_ACCOUNT root
ENV DB_PASSWORD redd00r
ENV REDIS_HOST 172.18.0.201
ENV REDIS_PORT 6379
ENV PERMANENT_SESSION_LIFETIME 7200
ENV AUTHLIB_INSECURE_TRANSPORT 1
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
WORKDIR /var/www/html
ADD . /var/www/html
RUN pip3 install -r requirements.txt

CMD ["/var/www/html/init.sh"]

