from django.core.cache import cache
from rest_framework.response import Response
from typing import Callable
from rest_framework.generics import get_object_or_404



def process_request_or_cache(throttled_function: Callable[..., Response], request, timeout: int=60*60*3,*args, **kwargs) -> Response:
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


class MultipleFieldsQueryset:
    """
    Allow for multiple fields to lookup
    """
    # edited function from DRF source code:
    def get_object(self):
        """
        Returns the object the view is displaying.
        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        # lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        # filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # create filter using
        filter_kwargs = {key: self.kwargs[key] for key in self.kwargs if key in self.lookup_field}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
