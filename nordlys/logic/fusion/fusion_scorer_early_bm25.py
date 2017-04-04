"""
Early fusion scorer (i.e., object-centric model using BM25).

@author: Shuo Zhang
@author: Krisztian Balog
"""
from nordlys.logic.fusion.fusion_scorer import FusionScorer
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.retrieval_results import RetrievalResults
from collections import Counter
import math
import snowballstemmer

stemmer = snowballstemmer.stemmer('english')


class EarlyFusionScorer(FusionScorer):
    def __init__(self, index_name, association_file, object_length_file,
                 assoc_mode, retr_params, field="content", run_id="fusion"):
        """

        :param index_name: name of index
        :param association_file: document-object association file
        :param object_length_file: object length file
        :param assoc_mode: document-object weight mode, uniform or binary
        :param retr_params: BM25 parameter dict
        :param field: field to be searched
        """
        self._index_name = index_name
        self._elastic = Elastic(self._index_name)
        self._k1 = retr_params.get("k1", 1.2)
        self._b = retr_params.get("b", 0.75)
        self._field = field
        self._o_l = object_length(object_length_file)
        self._collection_length = self._elastic.coll_length(self._field)
        self._N = self._elastic.num_docs()
        self._assoc_mode = assoc_mode
        self.association_file = association_file
        self.assoc_doc = {}
        self.assoc_obj = {}
        self.run_id = run_id

    def score_query(self, query):
        """
        Scores a given query.

        :param query: query to be searched
        :return: pqo
        """
        aquery = self._elastic.analyze_query(query)
        pr = self._elastic.search(aquery, self._field)
        avg_ol = self._collection_length / (len(self.assoc_obj))
        q = self.parse(aquery)

        # Scoring objects, i.e., computing P(q|o)
        pqo = {}
        qt = Counter(q)
        for t, ftq in qt.items():
            # Scores each query term and sums up, i.e., computing P(t|o)

            # Retrieving documents and gets IDF
            n = len(self._elastic.search(t, self._field))  # number of documents containing term t
            if n == 0:
                continue
            idf = math.log((self._N - n + 0.5) / (n + 0.5))

            # Fuses f(t,o) for each object
            term = stemmer.stemWords(t.split())[0]
            ftd_fused = {}
            for item in pr.keys():
                doc_id = item
                if doc_id in self.assoc_doc:
                    try:
                        ftd = self._elastic.term_freq(doc_id, term, self._field)
                    except: # doc without content
                        ftd = 0
                    for object_id in self.assoc_doc[doc_id]:
                        if self._assoc_mode == FusionScorer.ASSOC_MODE_BINARY:
                            w_do = 1
                        elif self._assoc_mode == FusionScorer.ASSOC_MODE_UNIFORM:
                            w_do = 1 / len(self.assoc_obj[object_id])
                        else:
                            w_do = 0  # this should never happen
                        ftd_fused[object_id] = ftd_fused.get(object_id, 0) + ftd * w_do

            # Add pto into pqo
            for object_id in self.assoc_obj.keys():
                ol = int(self._o_l[object_id])
                fftd = ftd_fused.get(object_id, 0)
                score = (fftd * (self._k1 + 1)) / (fftd + self._k1 * (1 - self._b + self._b * ol / avg_ol))
                pqo[object_id] = pqo.get(object_id, 0) + idf * score

        return RetrievalResults(pqo)


def object_length(object_length_file):
    o_l = {}
    f = open(object_length_file, "r")
    for line in f:
        object_id, object_len = line.split("\t")
        o_l[object_id] = object_len
    return o_l
