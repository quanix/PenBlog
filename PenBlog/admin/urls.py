#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PenBlog.admin import article

__author__ = 'lihaoquan'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    # 文章
    url(r'^$', article.show_articles),
    # 分类

    # 连接

    # 设置
)
