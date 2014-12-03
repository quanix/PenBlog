# encoding: utf-8

__author__ = 'Home'


class CheckIsAdminMiddleware(object):
    def process_view(self, request, view, args, kwargs):


        return None

def is_admin(user, request):
    blog = get_current_blog(request)

    return False