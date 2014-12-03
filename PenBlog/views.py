#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from PenBlog.config.server import *
from PenBlog.func import *

__author__ = 'quanix'

def show_homepage(request, page):

    db = connect_mongodb_database(request)

    info = db.infos.find_one()

    page = int(page)

    return render_and_back(request, 'index.html', {
        'page': '首页'
    })



def install(request):

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