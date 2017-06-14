#!/usr/bin/env python

import base64
import httplib
import json
import os
import sys
from request import HttpRequest

class OSDF(object):
    """
    Communicates with an OSDF server's REST interface to facilitate several
    operations (node creation, deletion, queries, etc.)
    """

    def __init__(self, server, username, password, port=8123, ssl=False):
        self._server = server
        self._port = port
        self._username = username
        self._password = password
        self._ssl = ssl
        self._set_request()

    def _set_request(self):
        self._request = HttpRequest(self._server, self._username,
                                    self._password, self._port,
                                    self._ssl)

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._server = server
        # Redefine the request object
        self._set_request()

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port
        # Redefine the request object
        self._set_request()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
        # Redefine the request object
        self._set_request()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        # Redefine the request object
        self._set_request()

    @property
    def ssl(self):
        return self._ssl

    @ssl.setter
    def ssl(self, ssl):
        if type(ssl) is not bool:
            raise ValueError("Invalid value for ssl.")

        self._ssl = ssl
        # Redefine the request object
        self._set_request()

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
            self.header_error(headers, 'edit', 'node')

    def _byteify(self, input):
        if isinstance(input, dict):
            return {self._byteify(key):self._byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [self._byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def get_info(self):
        """
        Retrieve's the OSDF server's information/contact document
        """
        osdf_response = self._request.get("/info")

        info = json.loads( osdf_response['content'] )

        info = self._byteify(info)

        return info

    def get_node(self, node_id):
        """
        Retrieves an OSDF node given the node's ID

        Returns the parsed form of the JSON document for the node
        """
        osdf_response = self._request.get("/nodes/" + node_id)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'node')

        data = json.loads( osdf_response['content'] )

        data = self._byteify(data)

        return data

    def get_nodes_in(self, node_id):
        """
        Retrieves the nodes that link to the OSDF node identified by the
        given the node ID.

        """
        url = "/nodes/{}/in".format(node_id)
        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'node')

        data = json.loads( osdf_response['content'] )

        data = self._byteify(data)

        return data

    def get_nodes_out(self, node_id):
        """
        Retrieves the OSDF nodes that the given node links to (via it's linkage
        field).
        """
        url = "/nodes/{}/out".format(node_id)
        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'node')

        data = json.loads( osdf_response['content'] )

        data = self._byteify(data)

        return data

    def get_node_by_version(self, node_id, version):
        """
        Given a numerical version number, retrieves an OSDF node's data
        as it was at that version.

        Returns the parsed form of the JSON document for the node
        """
        osdf_response = self._request.get("/nodes/%s/ver/%s" % (node_id, version))

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'node')

        data = json.loads( osdf_response['content'] )

        data = self._byteify(data)

        return data

    def get_schemas(self, namespace):
        """
        Retrieves all of the schemas for a particular namespace.
        """
        url = '/namespaces/%s/schemas/' % namespace

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'schemas')

        all_schema_data = json.loads( osdf_response['content'] )

        schema_data = self._byteify(all_schema_data)

        return all_schema_data

    def get_schema(self, namespace, schema_name):
        """
        Retrieves a namespace's document schema

        Returns the parsed form of the JSON-Schema document
        """
        url = '/namespaces/%s/schemas/%s' % (namespace, schema_name)

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'schema')

        schema_data = json.loads( osdf_response['content'] )

        schema_data = self._byteify(schema_data)

        return schema_data

    def get_aux_schemas(self, namespace):
        """
        Retrieves all of the auxiliary schemas for a particular namespace.

        Returns the parsed form of the auxiliary schemas.
        """
        url = '/namespaces/%s/schemas/aux/' % (namespace)

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'aux schemas')

        aux_schema_data = json.loads( osdf_response['content'] )

        aux_schema_data = self._byteify(aux_schema_data)

        return aux_schema_data

    def get_aux_schema(self, namespace, aux_schema_name):
        """
        Retrieves an auxiliary schema

        Returns the parsed form of the auxiliary schema JSON
        """
        url = '/namespaces/%s/schemas/aux/%s' % (namespace, aux_schema_name)

        osdf_response = self._request.get(url)

        if osdf_response["code"] != 200:
            headers = osdf_response['headers']
            self.header_error(headers, 'retrieve', 'aux schema')

        aux_schema_data = json.loads( osdf_response['content'] )

        aux_schema_data = self._byteify(aux_schema_data)

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

        if osdf_response['code'] != 204:
            headers = osdf_response['headers']
            self.header_error(headers, 'delete', 'node')

    def validate_node(self, json_data):
        """
        Report whether a node document validates against OSDF and its notion
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

    def oql_query(self, namespace, query, page=1):
        """
        Issue an OSDF Query Language (OQL) query against OSDF.

        Returns the specified page of results.
        """
        url = "/nodes/oql/%s/page/%s" % (namespace, str(page))

        osdf_response = self._request.post(url, query)

        if osdf_response["code"] != 200 and osdf_response["code"] != 206:
            headers = osdf_response["headers"]

            if 'x-osdf-error' in headers:
                msg = "Unable to query namespace %s. Reason: %s" % (namespace, headers['x-osdf-error'])
            else:
                msg = "Unable to query namespace."

            raise Exception(msg)

        data = json.loads( osdf_response['content'] )

        data = self._byteify(data)

        return data

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

        data = self._byteify(data)

        return data

    def oql_query_all_pages(self, namespace, query):
        """
        Issue an OSDF Query Language (OQL) query against OSDF, as in the
        oql_query() method, but retrieves ALL results by aggregating all
        the available pages of results. Use with caution, as this may
        consume a lot of memory with large result sets.
        """
        more_results = True
        page = 1
        cumulative_results = []

        while more_results:
           results = self.oql_query(namespace, query, page)

           cumulative_results.extend(results['results'])

           if results['result_count'] > 0:
               page += 1
           else:
               more_results = False

        results['results'] = cumulative_results
        results['result_count'] = len(results['results'])
        del results['page']

        return results;

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

    def header_error(self, headers=[], method_type='retrieve',
            document_type=None):
        if 'x-osdf-error' in headers:
            msg = "Unable to %s %s document. Reason: %s" \
                % (method_type, document_type, headers['x-osdf-error'])
        else:
            msg = "Unable to %s %s document." \
                % (method_type, document_type)

        raise Exception(msg)

