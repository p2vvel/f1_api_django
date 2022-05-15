from django.core.cache import cache
from rest_framework.response import Response
from typing import Callable



def process_request_or_cache(throttled_function: Callable[..., Response], request, timeout: int=2,*args, **kwargs) -> Response:
    """
    Check if result of function given as parameter has already been cached,
    if yes, return reponse with cache content, else - save function 
    result to cache and return response with this data

    Args:
        throttled_function (Callable[..., Response]): function to process or get result from cache
        request: request

    Returns:
        Response: result of given function - processed or retrieved from cache
    """
    url_path = request.get_full_path()      # request url (used as cache key)
    cache_data = cache.get(url_path)        # try fetching data from cache
    if cache_data:
        # return Response with data from cache
        return Response(cache_data)
    else:
        # data not found in cache - save it
        response = throttled_function(request, *args, **kwargs)
        cache.set(url_path, response.data, timeout=timeout)                  # cache result
        return response         # return requested data


class ReadOnlyModelViewsetCacheMixin:
    """
    Mixin used for caching of ReadOnlyModelViewsets requests
    """
    def list(self, request, *args, **kwargs):
        return process_request_or_cache(super().list, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return process_request_or_cache(super().retrieve, request, *args, **kwargs)

