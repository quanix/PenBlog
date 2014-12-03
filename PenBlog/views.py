#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PenBlog.func import render_and_back

__author__ = 'quanix'

def home(request, text):
    print 'text:'+text

    return render_and_back(request,'index.html',{})
