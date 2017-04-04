# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:53:45 2016

@author: sure
"""
'''
 -This is a statistic test file using the framework of unittest
 -This file includes the test cases for term statistics:
    -term frequency in doc
    -doc length
    -term frequency in collection
    -collection length
'''

import unittest
from nordlys.core.retrieval.elastic import Elastic
import snowballstemmer  # elastis uses snowballstemmer
import time

stemmer = snowballstemmer.stemmer('english')


class Statistics(object):
    index_name = "blog_test6"
    elastic = Elastic(index_name)

    def __init__(self):
        self.index_name = self.index_name

    def TF(self, term, doc_id, field):  # return term frequency in doc
        stat = self.elastic.get_termvector_all(docid=doc_id)
        term1 = stemmer.stemWords(term.split())[0]
        if field == "title":
            try:
                tf_title = stat['term_vectors']['title']['terms'][term1]['term_freq']
            except:
                tf_title = 0
            return tf_title
        elif field == "content":
            try:
                tf_con = stat['term_vectors']['content']['terms'][term1]['term_freq']
            except:
                tf_con = 0
            return tf_con

    def DL(self, doc_id, field):  # return doc length
        stat = self.elastic.get_termvector_all(docid=doc_id)
        if field == "title":
            dl = stat['term_vectors']['title']['field_statistics']['sum_ttf']
            return dl
        elif field == "content":
            dl_c = stat['term_vectors']['content']['field_statistics']['sum_ttf']
            return dl_c

    def TF_C(self, term, field):  # return term frequency in collection
        tf_c_t = 0
        tf_c_c = 0
        pr = self.elastic.search_all(self.index_name, term, fields_return="", start=0, num=100)['hits']
        if field == "content":
            for item in pr:
                record = self.elastic.get_termvector_all(docid=item['_id'])
                term1 = stemmer.stemWords(term.split())[0]
                try:
                    tf_c_c += record['term_vectors']['content']['terms'][term1]['term_freq']
                except:
                    tf_c_c += 0
            return tf_c_c
        elif field == "title":
            for item in pr:
                record = self.elastic.get_termvector_all(docid=item['_id'])
                term1 = stemmer.stemWords(term.split())[0]
                try:
                    tf_c_t += record['term_vectors']['title']['terms'][term1]['term_freq']
                except:
                    tf_c_t += 0
            return tf_c_t

    def CL(self, term, field):  # return collection length
        cl_t = 0
        cl_c = 0
        pr = self.elastic.search_all(self.index_name, term, fields_return="", start=0, num=100)['hits']
        for item in pr:
            record = self.elastic.get_termvector_all(docid=item['_id'])
            cl_t = cl_t + record['term_vectors']['title']['field_statistics']['sum_ttf']
            cl_c = cl_c + record['term_vectors']['content']['field_statistics']['sum_ttf']
        if field == "title":
            return cl_t
        elif field == "content":
            return cl_c


class TestStatistics(unittest.TestCase):
    mappings = {
        "id": {
            "type": "string",
            "index": "not_analyzed"
        },
        "title": {
            "type": "string",
            "term_vector": "with_positions_offsets",
            "analyzer": "english"
        },
        "content": {
            "type": "string",
            "term_vector": "with_positions_offsets",
            "analyzer": "english"
        }
    }

    docs = {
        1: {"title": "t1 t2",
            "content": "t1 t2 t3 t4 t1"
            },
        2: {"title": "t2",
            "content": "t1 t1 t3 t5"
            }
    }
    tf = {
        1: {"title": {"t1": 1, "t2": 1},
            "content": {"t1": 2, "t2": 1, "t3": 1, "t4": 1}
            },
        2: {"title": {"t2": 1},
            "content": {"t1": 2, "t3": 1, "t5": 1}
            }
    }
    cf = {
        "title": {
            "t1": 1,
            "t2": 2
        },
        "content": {
            "t1": 4,
            "t2": 1,
            "t3": 2,
            "t4": 1,
            "t5": 1
        }
    }
    dl = {
        1: {"title": 2,
            "content": 5
            },
        2: {"title": 1,
            "content": 4
            }
    }
    cl = {
        "t1": {"title": 3,
               "content": 9
               },
        "t4": {"title": 2,
               "content": 5
               },
        "t5": {"title": 1,
               "content": 4
               }

    }

    def setUp(self):
        '''
        set up the test cases; index docs
        '''
        super(TestStatistics, self).setUp()
        self.statistics = Statistics()
        self.elastic = self.statistics.elastic
        self.elastic.create_index(mappings=self.mappings, force=False)
        self.elastic.add_docs_bulk(self.docs)
        time.sleep(1)  # indexing needs some time,otherwise excuting test without index

    def test_statistics(self):
        '''
        test Statistics.TF(): term frequency 
        '''
        print("Test Statistics.TF()")
        for docid, term_dict in self.tf.items():
            for field, statis in term_dict.items():
                for term, num in statis.items():
                    self.assertEqual(self.statistics.TF(term, docid, field), num)

        '''
        test Statistics.TF_C(): collection term frequency
        '''
        print("Test Stastistics.TF_C()")
        for field, stat in self.cf.items():
            for term, num in stat.items():
                self.assertEqual(self.statistics.TF_C(term, field), num)

        '''
        test Statistics.DL(): document length
        '''
        print("Test Statistics.DL()")
        for docid, lg_dict in self.dl.items():
            for field, lg in lg_dict.items():
                self.assertEqual(self.statistics.DL(docid, field), lg)

        '''
        test Statistic.CL(): collection length
        '''
        print("Test Statistics.CL()")

        for term, cl_dict in self.cl.items():
            for field, lg in cl_dict.items():
                self.assertEqual(self.statistics.CL(term, field), lg)

            #    def test_statistics_clean_up(self):
        '''
        delete the used index
        '''
        self.elastic.delete_index()


if __name__ == '__main__':
    unittest.main()
