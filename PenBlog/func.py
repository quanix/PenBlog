#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from pymongo import Connection
import pytz
from PenBlog.config.server import BLOGS, STR_NAME, DATABASE_USERNAME, DATABASE_PORT, DATABASE_HOST, DATABASE_PASSWORD

__author__ = 'quanix'


def connect_mongodb_account_database(request):
    """
    连接到账户数据库
    """
    # 缺省连接到本地数据库
    if DATABASE_USERNAME is None:
        host = 'mongodb://%s:%d' % (DATABASE_HOST, DATABASE_PORT)
    else:
        host = 'mongodb://%s:%s@%s:%d' %\
               (DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)

    c = Connection(host)
    return c['penblog_users']



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

    return c['penblog_blogs_' + name]

def get_upload_path(name):
    return os.path.join(os.path.dirname(__file__), 'upload', name)


def get_themes():
    """
    获取主题
    :return:
    """
    directory = os.path.join(os.path.dirname(__file__), 'themes')
    return os.listdir(directory)

def set_template_dir(*d):
    """
    设置项目模板
    :param d:
    :return:
    """
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


def render_admin_and_back(request, template, d):
    """
    渲染博客的管理页面
    """

    db = connect_mongodb_database(request)
    info = db.infos.find_one()

    # 设定模板目录
    set_template_dir('admin')

    # 增加项
    d['title'] = info['Title']
    d['host'] = request.get_host()
    d['user'] = request.session.get('user')

    # 渲染模板
    t = get_template(template)
    html = t.render(Context(d))

    # 关闭数据库
    #db.connection.close()

    return HttpResponse(html)


def query_mine_type(ext):
    """
    获取文件的mine格式
    :param ext:
    :return:
    """
    d = {
        'css': 'text/css',
        'js': 'application/x-javascript',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'gif': 'image/gif',
        'xml': 'text/xml',
        'swf': 'application/x-shockwave-flash',
        'html': 'text/html',
    }

    if ext in d:
        return d[ext]

    return ''

def redirect(request, title, path=None, delay=200):
    """
    重定向
    """
    set_template_dir('admin')
    if path is None:
        path = request.get_full_path()[1:]
    return render_to_response('redirect.html', {
        'host':request.get_host(),
        'title': title,
        'redirect': path,
        'delay': delay
    })


def ensure_index_of_blog(db):
    """
    创建博客数据库的索引
    """
    db.articles.ensure_index([('Id', -1)])
    db.articles.ensure_index([('PostOn', -1)])
    db.articles.ensure_index([('IsPublic', -1)])
    db.articles.ensure_index('Tags')
    db.articles.ensure_index('Categories')
    db.categories.ensure_index([('Title', 1)])



##### Time Hadnle ######

def get_utc_from_local(dt, timezone):
    if timezone not in pytz.all_timezones:
        return dt

    # 验证客户端给出的时区是否有效
    tz = pytz.timezone(timezone)
    utc = pytz.utc.normalize(tz.localize(dt))
    return utc

def get_local_from_utc(dt, timezone):
    if timezone not in pytz.all_timezones:
        return dt

    # 验证客户端给出的时区是否有效
    tz = pytz.timezone(timezone)
    local = tz.normalize(pytz.utc.localize(dt))
    return local

def calculate_local_time(info, article):

    # 取得时区
    article['Timezone'] = article.get('Timezone')
    timezone = article.get('Timezone') or info.get('DefaultTimezone')
    if timezone is None:
        return

    # 重新计算时间
    tz = pytz.timezone(timezone)
    postOn = article['PostOn']
    article['PostOn'] = tz.normalize(pytz.utc.localize(postOn))

    # 时差
    article['TimezoneOffset'] = article.get('TimezoneOffset')

    # 是否出于夏令时
    article['IsDst'] = tz.dst(postOn).seconds != 0

def calculate_local_timeinfo(info, article):

    # 取得时区
    timezone = article.get('Timezone') or info.get('DefaultTimezone')
    if timezone is None:
        return

    article['Timezone'] = timezone

    # 重新计算时间
    tz = pytz.timezone(timezone)
    postOn = article['PostOn']
    article['PostOn'] = tz.normalize(pytz.utc.localize(postOn))

    # 时差
    offset = article.get('TimezoneOffset') or info.get('DefaultTimezoneOffset')
    article['TimezoneOffset'] = offset

    # 是否出于夏令时
    article['IsDst'] = tz.dst(postOn).seconds != 0