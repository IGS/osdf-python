#!/usr/bin/env python

import unittest
from osdf import OSDF

class OsdfTest(unittest.TestCase):
    server = "osdf-devel.igs.umaryland.edu"
    username = "test"
    password = "test"

    def testGetInfo(self):
        osdf = OSDF(OsdfTest.server, OsdfTest.username, OsdfTest.password)

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
        osdf = OSDF(OsdfTest.server, OsdfTest.username, OsdfTest.password)

        query = '"project"[node_type]'
        namespace = "test"

        results = osdf.oql_query(namespace, query)

        self.assertIsNotNone(results, "OQL query result is not None.")

        self.assertTrue(type(results) == dict, "OQL query result is a list.")

        self.assertTrue('result_count' in results, "Result contains 'result_count' key.")
        self.assertTrue('results' in results, "Result contains 'results' key.")
        self.assertTrue('page' in results, "Result contains 'page' key.")

    def testQuery(self):
        osdf = OSDF(OsdfTest.server, OsdfTest.username, OsdfTest.password)

        query = '{ "term" : { "node_type" : "project" }}'
        namespace = "test"

        results = osdf.query(namespace, query)

        self.assertIsNotNone(results, "Query result is not None.")

        self.assertTrue(type(results) == dict, "Query result is a list.")

        self.assertTrue('result_count' in results, "Result contains 'result_count' key.")
        self.assertTrue('results' in results, "Result contains 'results' key.")
        self.assertTrue('page' in results, "Result contains 'page' key.")


if __name__ == "__main__":
    unittest.main()
