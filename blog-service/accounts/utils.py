from django.urls import reverse
from django.utils.http import urlencode


def build_url(*args, **kwargs):
    """Extend django's reverse to add custom get parameters."""
    get_params = kwargs.pop('get_params', None)
    # Provide fixed url if you need to build a url for external sites.
    # Else, each site point should be reversible through route names.
    url = kwargs.pop('url', None)

    if url is None:
        url = reverse(*args, **kwargs)

    if get_params:
        url += '?' + urlencode(get_params)

    return url

