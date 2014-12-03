PenBlog
=======

基于uWSGI+Nginx

用Centos做服务器，Nginx做WebServer，uwsgi做应用程序容器。

#环境要求
 * Python 2.6 / 2.7
 * Django >=1.4
 * MongoDB >=1.8.0

其他依赖的Python组件：
 * pymongo(2.2.1)
 * pytz(2012d)

Django、pymongo和pytz

    pip install django
    pip install pymongo
    pip install pytz

##启动方式

1. sudo nginx -c penblog_nginx.conf
2. uwsgi -d --ini penblog_uwsgi.ini