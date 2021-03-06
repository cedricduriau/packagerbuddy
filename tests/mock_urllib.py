# stdlib modules
try:
    from urllib.response import addinfourl
    from urllib.error import HTTPError
    from urllib.request import HTTPHandler
    from io import StringIO
except ImportError:
    from urllib2 import addinfourl, HTTPError, HTTPHandler
    from StringIO import StringIO


def mock_response(req):
    url = req.get_full_url()

    if url.startswith("http://valid"):
        resp = addinfourl(StringIO("valid"), "valid", url)
        resp.code = 200
        resp.msg = "OK"
        resp.headers = {"content-disposition": "filename=valid.tar"}
        return resp
    elif url.startswith("http://filename"):
        resp = addinfourl(StringIO("filename"), "filename", url)
        resp.code = 200
        resp.msg = "OK"
        resp.headers = {}
        return resp
    elif url.startswith("http://invalid"):
        raise HTTPError(url, 404, "invalid", "", StringIO())


class MockHTTPHandler(HTTPHandler):
    def http_open(self, req):
        return mock_response(req)
