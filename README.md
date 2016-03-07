[![PyPI version](https://img.shields.io/pypi/v/osdf-python.svg)](https://pypi.python.org/pypi/osdf-python)

# osdf-python

## Basic usage

    import pprint
    from osdf import OSDF

    server = "server.ip.dns.address"
    username = "user"
    password = "password"
    port = 8123

    osdf = OSDF(server, username, password, port)

    info = osdf.get_info()

    pprint.pprint(info)


## SSL/Encrypted connections

To establish a connection to an instance of OSDF that is encrypted by
operating with an SSL certificate, simply pass the a named ssl parameter
set to true.

    osdf = OSDF(server, username, password, port, ssl=True)

## Obtaining the server information

    info = osdf.get_info()

    pprint.pprint(info)

    {
      "api_version": "0.1",
      "title": "EXAMPLE-OSDF",
      "description": "Open Science Data Framework (OSDF)",
      "admin_contact_email1": "osdf-admin@example.edu",
      "admin_contact_email2": "help@example.edu",
      "technical_contact1": "osdf@example.edu",
      "technical_contact2": "osdf-helpdesk@example.edu",
      "comment1": "comment1",
      "comment2": "comment2"
    }

## Retrieve an existing node
One is able to retrieve a node by ID easily.

    node = osdf.get_node(node_id)

## Retrieve a previous version of an existing node
OSDF maintains the history of nodes as they change over time
from edit to edit. To retrieve a particular node at a specific
version number, simply pass the versoin number (as well as the node
id of interest) to the get_node_by_version() function.

    node = osdf.get_node_by_version(node_id, version)

## Validate a node document
Sometimes its useful to check if a document validates against the OSDF instance
to verify if the metadata in the document passes all the structural integrity
and other requirements. To validate a document, use the validate_node()
function, and pass the JSON data as an argument. The return is a tuple with the
first value containing a boolean with the result of the validation, and the
second value will contain the error message (if the document was not valid).

   (is_valid, error) = osdf.validate_node(json_data)
    
## Inserting a node
The creation/insertion of a new node returns the node's ID.

    document = {
                  "ns": "test",
                  "acl": { "read": [ "all" ], "write": [ "all" ] },
                  "linkage": {},
                  "node_type": "example",
                  "meta": {
                      "description": "something",
                      "color": "blue"
                  }
              }

    node_id = osdf.insert_node(document)

## Edit/Update a node
Updates an existing node document with new/edited data. OSDF will save the
older data to the node's history, and it will be available for retrieval
by version number. The provided node data must contain the node ID as well
as the current version number of the node, so as to avoid conflicts with others
that may be attempting to edit that document.

    osdf.edit_node(node_data)

## Deleting a node
To delete a node, simply call the delete_node() function. This action also
removes the historical information associated with that node (previous
versions).

    osdf.delete_node(node_id)

## ElasticSearch DSL queries
     namespace = "test"
     query = '{ "query": { "term": { "node_type": "example" }} }'
     first_page_results = osdf.query(namespace, query)
     # If there are more than 1 "page" of results, additional results
     # can be obtained...
     second_page_results = osdf.query(namespace, query, 2)

To retrieve ALL results by aggregating all the available pages of results

    all_results = osdf.query_all_pages(namespace, query)
     
## OQL (OSDF Query Language) queries
OSDF also supports a simplified query language called OQL (OSDF Query Language). To issue
an OQL query:

     namespace = "test"
     query = '"example"[node_type]'
     first_page_results = osdf.oql_query(namespace, query, 1)
     # If there are more than 1 "page" of results, additional results
     # can be obtained...
     second_page_results = osdf.oql_query(namespace, query, 2)
     
To retrieve ALL results by aggregating all the available pages of results

     all_results = osdf.oql_query_all_pages(namespace, query)

## Retrieve all schemas for a given namespace
Namespaces can impose controls on the JSON data contained in their nodes according
to the nodetype. To retrieve the complete set of registered schemas for a particular
namespace, use the get_schemas() function:

     schemas = osdf.get_schemas(namespace)
     
## Retrieve a specific schema
If a node type has a JSON-Schema associated with it, that specific schema
can be queried from OSDF using the get_schema() function by passing the name of
namespace as well as the name of the schema/node_type.

     schema = osdf.get_schema(namespace, schema_name)
     
## Retrieve an OSDF auxiliary schema
Schemas can share JSON-Schema fragments between them in order to avoid duplication.
These schema fragements are referred to as auxiliary schemas, and are also
retrievable with the get_aux_schema() function by passing the namespace and
auxiliary schema name.

     aux_schema = osdf.get_aux_schema(namespace, aux_schema_name)
    
