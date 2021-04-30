import re

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout as dj_logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    # compiles logout and register
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        #  pass / class works without problem only afer it has function
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # going to run when the django processes one of the functions
    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')  # has the urls defined
        # lstrip removes first / from path
        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        # if not request.user.is_authenticated:
        #     if not url_is_exempt:
        #         return redirect(settings.LOGIN_URL)

        if path == 'accounts/logout/':
            dj_logout(request)

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_AUTH_URL)

        elif request.user.is_authenticated or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_URL)
