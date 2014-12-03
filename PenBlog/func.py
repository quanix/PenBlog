#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

__author__ = 'quanix'


def set_template_dir(*d):

    settings.TEMPLATE_DIRS = (
        os.path.join(os.path.dirname(__file__), *d),
    )

    print settings.TEMPLATE_DIRS



def render_and_back(request, template, d):
    # 设定模板目录
    d['theme'] = 'Zine'
    set_template_dir('themes', d['theme'])
    t = get_template(template)
    html = t.render(Context(d))
    return HttpResponse(html)