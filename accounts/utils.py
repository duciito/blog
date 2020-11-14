from django.urls import reverse
from django.utils.http import urlencode


def build_url(*args, **kwargs):
    """Extend django's reverse to add custom get parameters."""
    get_params = kwargs.pop('get_params', None)
    url = reverse(*args, **kwargs)
    if get_params:
        url += '?' + urlencode(get_params)

    return url

