# stdlib modules
import urllib2
import StringIO


def mock_response(req):
    url = req.get_full_url()
    if url.startswith("http://valid.com"):
        resp = urllib2.addinfourl(StringIO.StringIO("valid"), "valid", url)
        resp.code = 200
        resp.msg = "OK"
        return resp
    elif url.startswith("http://invalid.com"):
        raise urllib2.HTTPError(url, 404, "invalid", "", StringIO.StringIO())


class MockHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return mock_response(req)
