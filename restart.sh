ps -ef | grep uwsgi | grep -v grep| awk '{print $2}' | xargs kill -9

uwsgi -d --ini PenBlog/penblog_uwsgi.ini

echo '重启成功'