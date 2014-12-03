#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PenBlog.func import render_and_back

__author__ = 'quanix'

def show_homepage(request, page):

    page = int(page)

    return render_and_back(request, 'index.html', {
        'page': '首页'
    })
