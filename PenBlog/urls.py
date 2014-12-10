#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()
from PenBlog import views

urlpatterns = patterns('',

    #首页
    url(r'^$', views.show_homepage, {'page': 1}),
    url( r'^page/(\d+?)/$', views.show_homepage),
    #调试时取得静态文件
    url(r'\.(css|js|png|jpg|gif|xml|swf|html)$', views.get_file),

    #安装页面
    url(r'^install/$', views.install),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^register/$', views.register),


    url(r'^article/(\d+?)/$', views.show_article),
    url(r'^category/(.+?)/$', views.show_category),
    url(r'^tag/(.+?)/$', views.show_tag),
    # 管理员页面
    url(r'^admin/', include('PenBlog.admin.urls')),
)
