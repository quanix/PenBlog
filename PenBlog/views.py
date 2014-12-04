#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from PenBlog.config.server import *
from PenBlog.func import *

__author__ = 'quanix'

def show_homepage(request, page):
    """
    博客首页
    :param request:
    :param page:
    :return:
    """

    db = connect_mongodb_database(request)

    info = db.infos.find_one()

    page = int(page)

    return render_and_back(request, 'index.html', {
        'page': '首页'
    })



def install(request):
    """
    安装页面
    :param request:
    :return:
    """
    blog = get_current_blog(request)

    admin = blog[STR_ADMINS]

    admins = blog[STR_ADMINS]
    if isinstance(admin, list):
        admins = ', '.join(admins)

    set_template_dir('admin')
    return render_to_response('install.html', {
            'host':request.get_host(),
            'name': blog[STR_NAME],
            'admins': admins
        })



def get_file(request, ext):
    """
    获取静态文件
    :param request:
    :param ext:
    :return:
    """
    path = request.path
    abspath = os.path.abspath('.') + '/' + 'PenBlog' + path
    if os.sep != '/':
        abspath = abspath.replace('/', '\\')

    stream = open(abspath, 'rb').read()
    mine = query_mine_type(ext)

    return HttpResponse(stream, mimetype=mine)


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    if 'user' in request.session:
        del request.session['user']
    return redirect(request, '已退出', 'admin/', 0)