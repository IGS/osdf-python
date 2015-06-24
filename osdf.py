#!/usr/bin/env python

import base64
import httplib
import json
import os
import sys
from request import HttpRequest

class OSDF:
    """
    Communicates with an OSDF server's REST interface to facilitate several
    operations (node creation, deletion, queries, etc.)
    """

    def __init__(self, server, username, password, port=8123):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self._request = HttpRequest(server, username, password, port=port)

    @property
    def server(self):
        return self.server

    @server.setter
    def server(self, server):
        self.server = server
        # Redefine the request object
        self._request = HttpRequest(self.server, self.username,
                                    self.password, self.port)

    @property
    def port(self):
        return self.port

    @server.setter
    def port(self, port):
        self.port = port
        # Redefine the request object
        self._request = HttpRequest(self.server, self.username,
                                    self.password, self.port)

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, username):
        self.username = username
        # Redefine the request object
        self._request = HttpRequest(self.server, self.username,
                                    self.password, self.port)

    @property
    def password(self):
        return self.password

    @password.setter
    def username(self, username):
        self.password = password
        # Redefine the request object
        self._request = HttpRequest(self.server, self.username,
                                    self.password, self.port)

    def edit_node(self, json_data):
        """
        Updates a node with the provided data
        """
        # Get the node id from json_data
        if 'id' not in json_data:
            raise Exception("No node id in the provided JSON.")

        node_id = json_data['id']

        json_str = json.dumps(json_data);

        osdf_response = self._request.put("/nodes/" + node_id, json_str)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']

            if 'x-osdf-error' in headers:
                msg = "Unable to edit node document. Reason: " \
                      + headers['x-osdf-error']
                raise Exception(msg)
            else:
                raise Exception("Unable to edit node document.")

    def get_info(self):
        """
        Retrieve's the OSDF server's information/contact document
        """
        osdf_response = self._request.get("/info")

        info = json.loads( osdf_response['content'] )

        return info

    def get_node(self, node_id):
        """
        Retrieves an OSDF node given the node's ID

        Returns the parsed form of the JSON document for the node
        """
        osdf_response = self._request.get("/nodes/" + node_id)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']

            if 'x-osdf-error' in headers:
                msg = "Unable to retrieve node document. Reason: " \
                      + headers['x-osdf-error']
            else:
                msg = "Unable to retrieve node document."

            raise Exception(msg)

        data = json.loads( osdf_response['content'] )

        return data

    def get_schema(self, namespace, schema_name):
        """
        Retrieves a namespace's document schema

        Returns the parsed form of the JSON-Schema document
        """
        url = '/namespaces/%s/schemas/%s' % (namespace, schema_name)

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']

            if 'x-osdf-error' in headers:
                msg = "Unable to retrieve schema document. Reason: " \
                      + headers['x-osdf-error']
            else:
                msg = "Unable to retrieve schema document."

            raise Exception(msg)

        schema_data = json.loads( osdf_response['content'] )

        return schema_data

    def get_aux_schema(self, namespace, aux_schema_name):
        """
        Retrieves an auxiliary schema

        Returns the parsed form of the auxiliary schema JSON
        """
        url = '/namespaces/%s/schemas/aux/%s' % (namespace, aux_schema_name)

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']

            if 'x-osdf-error' in headers:
                msg = "Unable to retrieve schema document. Reason: " \
                      + headers['x-osdf-error']
            else:
                msg = "Unable to retrieve schema document."

            raise Exception(msg)

        aux_schema_data = json.loads( osdf_response['content'] )

        return aux_schema_data

    def insert_node(self, json_data):
        """
        Inserts a node with the provided data into OSDF

        Returns the node ID upon successful insertion.
        """
        json_str = json.dumps(json_data);

        osdf_response = self._request.post("/nodes", json_str)
        node_id = None

        headers = osdf_response["headers"]

        if osdf_response["code"] == 201:
            if 'location' in headers:
                node_id = headers['location'].split('/')[-1]
            else:
                raise Exception("No location header for the newly inserted node.")
        else:
            if 'x-osdf-error' in headers:
                msg = "Unable to insert node document. Reason: " + headers['x-osdf-error']
            else:
                msg = "Unable to insert node document."

            raise Exception(msg)

        return node_id

    def delete_node(self, node_id):
        """
        Deletes the specified node from OSDF.
        """
        osdf_response = self._request.delete("/nodes/" + node_id)

        if osdf_response['code'] != 200:
            if 'x-osdf-error' in headers:
                msg = "Unable to delete node document. Reason: " + headers['x-osdf-error']
            else:
                msg = "Unable to delete node document."

            raise Exception(msg)

    def validate_node(self, json_data):
        """
        Report whether a node document validates against OSDF and it's notion
        of what that node should look like according to any registered schemas.

        Returns a tuple with the first value holding a boolean of whether the
        document validated or not. The second value contains the error message
        if the document did not validate.
        """
        json_str = json.dumps(json_data);
        url = "/nodes/validate"

        osdf_response = self._request.post(url, json_str)
        headers = osdf_response["headers"]
        valid = False

        error_msg = None

        if osdf_response["code"] != 200:
            if 'x-osdf-error' in headers:
                error_msg = headers['x-osdf-error']
            else:
                error_msg = "Unknown"
        else:
            valid = True

        return (valid, error_msg)


    def query(self, namespace, query, page=1):
        """
        Issue a query against OSDF. Queries are expressed in JSON form using
        the ElasticSearch Query DSL.

        Returns the specified page of results.
        """
        url = "/nodes/query/%s/page/%s" % (namespace, str(page))

        osdf_response = self._request.post(url, query)

        if osdf_response["code"] != 200 and osdf_response["code"] != 206:
            headers = osdf_response["headers"]

            if 'x-osdf-error' in headers:
                msg = "Unable to query namespace %s. Reason: %s" % (namespace, headers['x-osdf-error'])
            else:
                msg = "Unable to query namespace."

            raise Exception(msg)

        data = json.loads( osdf_response['content'] )

        return data

    def query_all_pages(self, namespace, query):
        """
        Issue a query against OSDF, as in the query() method, but retrieves
        ALL results by aggregating all the available pages of results. Use with
        caution, as this may consume a lot of memory with large result sets.
        """
        more_results = True
        page = 1
        cumulative_results = []

        while more_results:
           results = self.query(namespace, query, page)

           cumulative_results.extend(results['results'])

           if results['result_count'] > 0:
               page += 1
           else:
               more_results = False

        results['results'] = cumulative_results
        results['result_count'] = len(results['results'])
        del results['page']

        return results;

    def create_osdf_node(self, namespace, node_type, domain_json, linkage={}, read="all", write="all"):
        node_json = { 'ns': namespace,
                      'acl': { 'read': [ read ], 'write': [ write ] },
                      'linkage': linkage,
                      'meta': domain_json,
                      'node_type': node_type }

        return node_json
