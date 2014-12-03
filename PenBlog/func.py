#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from pymongo import Connection
from PenBlog.config.server import BLOGS, STR_NAME, DATABASE_USERNAME, DATABASE_PORT, DATABASE_HOST, DATABASE_PASSWORD

__author__ = 'quanix'


def get_current_blog(request):
    host = request.get_host()
    print 'current host:'+host
    return BLOGS.get(host)


def connect_mongodb_database(request):
    """
    建立mongodb的数据库连接
    :param request:
    :return:
    """
    blog = get_current_blog(request)
    if blog is None:
        return None

    name = blog[STR_NAME]

    host = None

    if DATABASE_USERNAME is None:
        host = 'mongodb://%s:%d' % (DATABASE_HOST, DATABASE_PORT)
    else:
        host = 'mongodb://%s:%s@%s:%d' %\
               (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

    c = Connection(host)

    return c['PenBlogDB_' + name]




def set_template_dir(*d):

    settings.TEMPLATE_DIRS = (
        os.path.join(os.path.dirname(__file__), *d),
    )

    print settings.TEMPLATE_DIRS



def render_and_back(request, template, d):
    """
    页面跳转
    :param request:
    :param template:
    :param d:
    :return:
    """

    db = connect_mongodb_database(request)

    print '>>>>数据库获取信息'

    info = db.infos.find_one(fields={
        'Theme': 1,
        'Title': 1,
        'Subtitle': 1,
        'Description': 1,
        'CustomRss': 1,
        'WeiboCode': 1,
        'CommentCode': 1,
        'LatestCommentsCode': 1,
        'StatisticsCode': 1,
        'StatisticsCodeInHead': 1
    })

    current_theme = 'Zine'

    set_template_dir('themes', current_theme)

    d['host'] = request.get_host()
    d['user'] = request.session.get('user')
    d['theme'] = current_theme

    if info is not None:
        # 增加项
        d['info'] = info
        d['title'] = info['Title']


    t = get_template(template)
    html = t.render(Context(d))

    # 关闭数据库
    db.connection.close()

    return HttpResponse(html)