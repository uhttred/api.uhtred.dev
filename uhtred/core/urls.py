from django.utils.http import urlencode
from django.urls import reverse as rv, resolve

from rest_framework.routers import (
    SimpleRouter,
    Route,
    DynamicRoute)


# gist from: https://gist.github.com/benbacardi/227f924ec1d9bedd242b
def reverse(viewname: str, urlconf=None, args=None, kwargs=None, current_app=None, query=None) -> str:
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = rv(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query:
        return '{}?{}'.format(base_url, urlencode(query))
    return base_url


class Router(SimpleRouter):

    routes = [
        # List route.
        Route(
            url=r'^{prefix}$',
            mapping={
                'options': 'options',
                'head': 'head',
                'get': 'get',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'patch',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={})
    ]
