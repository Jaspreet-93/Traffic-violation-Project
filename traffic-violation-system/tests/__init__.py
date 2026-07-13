# Init tests package
import httpx

original_httpx_init = httpx.Client.__init__

def patched_httpx_init(self, *args, **kwargs):
    kwargs.pop('app', None)
    original_httpx_init(self, *args, **kwargs)

httpx.Client.__init__ = patched_httpx_init
