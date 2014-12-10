#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import pymongo
from PenBlog.func import *

__author__ = 'lihaoquan'

ERROR='error'
SUCCEED = 'succeed'


ARTICLES_PER_PAGE = 20

def show_articles(request, page = 1):
    """
    展示文章
    """
    page = int(page)
    db = connect_mongodb_database(request)
    info = db.infos.find_one()
    articles = list(db.articles.find(
        sort = [('PostOn', pymongo.DESCENDING)],
        skip = (page - 1) * ARTICLES_PER_PAGE,
        limit = ARTICLES_PER_PAGE,
    ))

    for a in articles:
        calculate_local_time(info, a)


    article_count = db.articles.count()
    page_count = article_count / ARTICLES_PER_PAGE +\
                 (1 if article_count % ARTICLES_PER_PAGE else 0)

    # 计算页码
    page_range = []
    if page <= page_count:
        low = (page - 1) / 10 * 10 + 1 # 利用整数除法
        if low + 10 <= page_count:
            page_range = range(low, 10 + 1)
        else:
            page_range = range(low, page_count + 1)

    return render_admin_and_back(request, 'articles.html', {
        'page': u'文章',
        'articles': articles,
        'selection': 'articles',
        'page_current': page,
        'page_range': page_range,
        'page_count': page_count,
    })


@csrf_exempt
def new(request):
    """
    文章的创建
    """
    db = connect_mongodb_database(request)
    if request.method == 'GET':
        info = db.infos.find_one()
        return render_admin_and_back(request,'edit-article.html', {
            'page': u'新文章',
            'categories': db.categories.find(),
            'article': {
                'Timezone': info.get('DefaultTimezone'),
                'TimezoneOffset': info.get('DefaultTimezoneOffset'),
                'UseDefaultTimezone': False,
            }
        })
    elif request.method == 'POST':
        d = request.POST #获取post过来的参数



def get_article_content(d, postOn = None):
    """
    获取文章内容
    """
    title = d.get('title')
    if title is None or title == '':
        return None, ERROR+'文章标题不能为空'

    content = d.get('content')
    if content is None or title == '':
        return None, ERROR+'正文内容不能为空'

    #设置是否公开文章
    is_public = d.get('is-set-public') == 'true'

    a = {
        'Title': title,
        'IsPublic': is_public,
        'Content': content if is_public else None,
        'HiddenContent': content if not is_public else None,
    }

    #分类和处理tags
    def split_and_strip(s):
        return [i.strip() for i in s.split(',') if i != '']

    categories = d.get('categories') or ''
    a['Categories'] = split_and_strip(d['categories'])