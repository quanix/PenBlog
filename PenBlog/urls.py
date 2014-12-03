#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()
from PenBlog import views

urlpatterns = patterns('',
    # Examples:

    #首页
    url(r'^$', views.show_homepage, {'page': 1}),
    url( r'^install/$', views.install),
)
