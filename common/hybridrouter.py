from collections import OrderedDict
from django.urls import NoReverseMatch
from rest_framework import routers, views, reverse, response
from drf_spectacular.utils import extend_schema

class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self._api_view_urls = {}
        self.trailing_slash = '/?'  # Make trailing slash optional

    def add_api_view(self, name, url, methods=None):
        if methods is None:
            methods = ['GET']
        for method in methods:
            key = f"{name}_{method.lower()}"
            self._api_view_urls[key] = (url, method)

    def remove_api_view(self, name, method=None):
        if method:
            key = f"{name}_{method.lower()}"
            del self._api_view_urls[key]
        else:
            keys_to_remove = [key for key in self._api_view_urls if key.startswith(name)]
            for key in keys_to_remove:
                del self._api_view_urls[key]

    @property
    def api_view_urls(self):
        ret = {}
        ret.update(self._api_view_urls)
        return ret

    def get_urls(self):
        urls = super(HybridRouter, self).get_urls()
        for api_view_key, (url, method) in self._api_view_urls.items():
            urls.append(url)
        return urls

    def get_api_root_view(self, api_urls=None):
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)
        api_view_urls = self._api_view_urls

        class APIRootView(views.APIView):
            _ignore_model_permissions = True
            exclude_from_schema = True

            @extend_schema(responses=dict)
            def get(self, request, *args, **kwargs):
                ret = OrderedDict()
                namespace = request.resolver_match.namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse.reverse(
                            url_name,
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                    except NoReverseMatch:
                        continue
                # In addition to what had been added, now add the APIView urls
                for api_view_key, (url, method) in api_view_urls.items():
                    regex = url.pattern.regex
                    if regex.groups == 0:
                        url_name = url.name
                        if namespace:
                            url_name = namespace + ':' + url_name
                        ret[api_view_key] = reverse.reverse(
                            url_name,
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                    else:
                        ret[api_view_key] = "WITH PARAMS: " + regex.pattern
                return response.Response(ret)

        return APIRootView.as_view()

    def register_router(self, another_router):
        self.registry.extend(another_router.registry)
        if hasattr(another_router, "_api_view_urls"):
            self._api_view_urls.update(another_router._api_view_urls)
