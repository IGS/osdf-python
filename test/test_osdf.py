#!/usr/bin/env python

import unittest
import os
from osdf import OSDF

def _get_osdf():
    osdf = OSDF(OsdfTest.server, OsdfTest.username, OsdfTest.password)
    return osdf

class OsdfTest(unittest.TestCase):
    if "OSDF_SERVER" in os.environ:
        server = os.environ.get("OSDF_SERVER")
    else:
        raise Exception("Must define OSDF_SERVER environment variable.")

    if "OSDF_USER" in os.environ:
        username = os.environ.get("OSDF_USER")
    else:
        raise Exception("Must define OSDF_USER environment variable.")

    if "OSDF_PASSWD" in os.environ:
        password = os.environ.get("OSDF_PASSWD")
    else:
        raise Exception("Must define OSDF_PASSWD environment variable.")

    test_node = {
                  "ns": "test",
                  "acl": { "read": [ "all" ], "write": [ "all" ] },
                  "linkage": {},
                  "node_type": "example",
                  "meta": {
                      "description": "something",
                      "color": "blue"
                  }
              }

    def testGetInfo(self):
        osdf = _get_osdf()

        info = None

        try:
            info = osdf.get_info()
        except:
            pass

        self.assertIsNotNone(info, "Information retrieved is not null.")

        self.assertTrue(type(info) == dict)

        self.assertTrue('description' in info)
        self.assertTrue('title' in info)

        self.assertTrue('admin_contact_email1' in info)
        self.assertTrue('admin_contact_email2' in info)

        self.assertTrue('technical_contact1' in info)
        self.assertTrue('technical_contact2' in info)


    def testOqlQuery(self):
        osdf = _get_osdf()

        query = '"project"[node_type]'
        namespace = "test"

        results = osdf.oql_query(namespace, query)

        self._examine_paged_results(results, "OQL")

    def testOqlQueryAllPages(self):
        osdf = _get_osdf()

        query = '"project"[node_type]'
        namespace = "test"

        results = osdf.oql_query_all_pages(namespace, query)
        self._examine_all_results(results, "OQL")

    def _examine_all_results(self, results, search_type):
        self.assertIsNotNone(results, "%s query result is not None." % search_type)

        self.assertTrue(type(results) == dict, "%s query result is a list." % search_type)

        self.assertTrue('result_count' in results,
                        "%s result contains 'result_count' key." % search_type)

        self.assertTrue('results' in results,
                        "%s result contains 'results' key." % search_type)

    def _examine_paged_results(self, results, search_type):
        self.assertIsNotNone(results,
                        "%s query result is not None." % search_type)

        self.assertTrue(type(results) == dict,
                        "%s query result is a list." % search_type)

        self.assertTrue('result_count' in results,
                        "%s result contains 'result_count' key." % search_type)
        self.assertTrue('results' in results,
                        "%s result contains 'results' key." % search_type)
        self.assertTrue('page' in results,
                        "%s result contains 'page' key." % search_type)

    def testQuery(self):
        osdf = _get_osdf()

        query = '{ "term" : { "node_type" : "project" }}'
        namespace = "test"

        results = osdf.query(namespace, query)

        self._examine_paged_results(results, "ES QueryDSL")

    def testInsertNode(self):

        osdf = _get_osdf()

        exception_thrown = False;
        node_id = None

        try:
            node_id = osdf.insert_node(OsdfTest.test_node)
        except Exception as e:
            print(e)
            exception_thrown = True

        # Check that the insertion did not raise an exception
        self.assertFalse(exception_thrown);
        self.assertIsNotNone(node_id,
                        "Node ID for inserted data is not None.")
        self.assertTrue(type(node_id) == str,
                        "Node ID for inserted data is a string.")

    def testGetNode(self):
        osdf = _get_osdf()

        exception_thrown = False;
        node_id = osdf.insert_node(OsdfTest.test_node)
        retrieved = None

        try:
            retrieved = osdf.get_node(node_id)
        except Exception as e:
            exception_thrown = True

        # Check that there were no issues
        self.assertFalse(exception_thrown);

        # Check that the retrieval yeilded some data
        self.assertIsNotNone(retrieved);
        self.assertTrue(type(retrieved) == dict,
                        "Node retrieved has correct type.")

        # Check that the data has the right structure
        self.assertTrue('ns' in retrieved)
        self.assertTrue('meta' in retrieved)
        self.assertTrue('linkage' in retrieved)
        self.assertTrue('ver' in retrieved)
        self.assertTrue('acl' in retrieved)
        self.assertTrue('id' in retrieved)

        self.assertEqual(retrieved['id'], node_id,
                         "Retrieved node has the right ID.")

        # Do some cleanup after ourselves
        try:
            osdf.delete_node(node_id)
        except:
            # ignore any problems as they are not relevant to this
            # particular test
            pass

    def testDeleteNode(self):
        osdf = _get_osdf()

        exception_thrown = False;
        node_id = osdf.insert_node(OsdfTest.test_node)

        try:
            osdf.delete_node(node_id)
        except Exception as e:
            exception_thrown = True

        # Check that the deletion did not raise an exception
        self.assertFalse(exception_thrown);

        # Now verify that the deletion actually work. A node
        # retrieval on that node ID should faile...
        get_success = True
        try:
            osdf.get_node(node_id)
        except Exception as e:
            get_success = False

        self.assertFalse(get_success, "Deletion persisted in OSDF.")

    def testQueryAllPages(self):
        osdf = _get_osdf()

        query = '{ "term" : { "node_type" : "project" }}'
        namespace = "test"

        results = osdf.query_all_pages(namespace, query)

        self._examine_all_results(results, "ES QueryDSL")


if __name__ == "__main__":
    unittest.main()
