# encoding: utf-8
import urllib2
from django.http import HttpResponseRedirect
from PenBlog.config.server import STR_ADMINS
from PenBlog.func import get_current_blog

__author__ = 'Home'


class CheckIsAdminMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        module = view.__module__
        if module.find("PenBlog.admin.") == 0:
            url = urllib2.quote(request.get_full_path()[1:])

            user = request.session.get('user')
            if user is None or not is_admin(user, request):
                return HttpResponseRedirect('/login/?redirect='+url)

        return None

def is_admin(user, request):
    blog = get_current_blog(request)
    if blog is not None:
        admins = blog[STR_ADMINS]
        if isinstance(admins, str) and admins == user['Username']:
            return True
        elif isinstance(admins, list) and user['Username'] in admins:
            return True

    return False