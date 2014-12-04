#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PenBlog.func import render_and_back

__author__ = 'lihaoquan'

def show_articles(request, page = 1):
    """
    展示文章
    :param request:
    :param page:
    :return:
    """
    return render_and_back(request, 'index.html', {
        'page': '首页'
    })