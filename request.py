#!/usr/bin/env python

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

    def delete(self, resource):
        conn = httplib.HTTPConnection(self.server, self.port)

        conn.putrequest("DELETE", resource)
        self._set_auth_header(conn)
        conn.endheaders()
        resp = conn.getresponse()
        content = resp.read()

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

    def get(self, resource):
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.putrequest("GET", resource)
        self._set_auth_header(conn)
        conn.endheaders()
        resp = conn.getresponse()
        content = resp.read()

        raw_headers = resp.getheaders()

        for header in raw_headers:
            header_name = header[0]
            header_value = header[1]
            headers = {}
            headers[header_name] = header_value

        results = { "headers": headers,
                    "content": content,
                    "code": resp.status
                  }

        return results

    def put(self, resource, data):
        conn = httplib.HTTPConnection(self.server, self.port, True)
        conn.putrequest("PUT", resource)
        self._set_auth_header(conn)
        conn.putheader("Content-Length", "%d" % len(data))
        conn.endheaders()

        conn.send(data)

        resp = conn.getresponse()
        raw_headers = resp.getheaders()
        content = resp.read()

        resp_headers = {}

        for header in raw_headers:
            header_name = header[0]
            header_value = header[1]
            resp_headers[header_name] = header_value

        results = { "headers": resp_headers,
                    "content": content,
                    "code": resp.status
                  }

        return results

    def post(self, resource, data):
        conn = httplib.HTTPConnection(self.server, self.port, True)

        conn.putrequest("POST", resource)
        self._set_auth_header(conn)
        conn.putheader("Content-Length", "%d" % len(data))
        conn.endheaders()

        conn.send(data)

        resp = conn.getresponse()
        raw_headers = resp.getheaders()
        content = resp.read()

        resp_headers = {}

        for header in raw_headers:
            header_name = header[0]
            header_value = header[1]
            resp_headers[header_name] = header_value

        results = { "headers": resp_headers,
                    "content": content,
                    "code": resp.status
                  }

        return results

    def _set_auth_header(self, connection):
        # We don't use the base64.encodestring() method here becuase it automatically adds
        # newlines
        base64string = "Basic " + base64.b64encode('%s:%s' % (self.username, self.password))
        connection.putheader("Authorization", base64string)
