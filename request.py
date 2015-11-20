#!/usr/bin/env python

try:
    import http.client as httplib
except ImportError:
    import httplib

import base64

class HTTPStatusException(Exception):

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return "Error [%s]: %s" % (self.status, self.message)

class HttpRequest(object):

    def __init__(self, server, username, password, port=8123):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def putrequest(self, request, resource):
        conn = httplib.HTTPConnection(self.server, self.port)

        conn.putrequest(request, resource)
        self._set_auth_header(conn)
        conn.endheaders()
        resp = conn.getresponse()
        content = resp.read()

        headers = {}
        raw_headers = resp.getheaders()

        for header in raw_headers:
            header_name = header[0]
            header_value = header[1]
            headers[header_name] = header_value

        results = { "headers": headers,
                    "content": content,
                    "code": resp.status
                  }

        return results

    def delete(self, resource):
        return self.putrequest("DELETE", resource)

    def get(self, resource):
        return self.putrequest("GET", resource)

    def put(self, resource, data):
        return self.putrequest("PUT", resource)

    def post(self, resource, data):
        return self.putrequest("POST", resource)

    def _set_auth_header(self, connection):
        # We don't use the base64.encodestring() method here becuase it automatically adds
        # newlines
        base64string = "Basic " + base64.b64encode('%s:%s' % (self.username, self.password))
        connection.putheader("Authorization", base64string)

