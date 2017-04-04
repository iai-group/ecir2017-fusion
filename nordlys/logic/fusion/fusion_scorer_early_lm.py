"""
Early fusion scorer (i.e., object-centric model using language modeling).

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
    def __init__(self, index_name, association_file, assoc_mode, retr_params, run_id="fusion", field="content",
                 num=100):
        """

        :param index_name: name of index
        :param association_file: document-object association file
        :param assoc_mode: document-object weight mode, uniform or binary
        :param lambda: smoothing parameter
        :param field: field to be searched
        """
        self._index_name = index_name
        self._elastic = Elastic(self._index_name)
        self._lambda = retr_params.get("lambda", 0.1)
        self._field = field
        self._collection_length = self._elastic.coll_length(self._field)
        self._assoc_mode = assoc_mode
        self._num = num
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
        # retrieving documents
        aquery = self._elastic.analyze_query(query)
        pr = self._elastic.search(aquery, self._field, num=self._num)
        q = self.parse(aquery)

        # scoring objects, i.e., computing P(q|o)
        pqo = {}
        qt = Counter(q)
        for t, ftq in qt.items():
            # Scores each query term and sums up, i.e., computing P(t|o)

            # Gets term frequency in collections
            term = stemmer.stemWords(t.split())[0]
            try:
                ftc = self._elastic.coll_term_freq(term, self._field)
                if ftc == None:
                    print("Ignore term", t)
                    continue
            except:
                print("Ignore term", t)
                continue

            ptc = ftc / self._collection_length

            # Fuses ptd for each object
            ptd_fused = {}
            for item in pr.keys():
                doc_id = item
                if doc_id in self.assoc_doc:
                    try:
                        ftd = self._elastic.term_freq(doc_id, term, self._field)
                    except: # the content of doc is empty
                        ftd = 0
                    doc_length = self._elastic.doc_length(doc_id, self._field)
                    ptd = ftd / doc_length
                    for object_id in self.assoc_doc[doc_id]:
                        if self._assoc_mode == FusionScorer.ASSOC_MODE_BINARY:
                            w_do = 1
                        elif self._assoc_mode == FusionScorer.ASSOC_MODE_UNIFORM:
                            w_do = 1 / len(self.assoc_obj[object_id])
                        else:
                            w_do = 0  # this should never happen
                        ptd_fused[object_id] = ptd_fused.get(object_id, 0) + ptd * w_do

            # Adds pto to pqo
            for object_id in self.assoc_obj.keys():
                fptd = ptd_fused.get(object_id, 0)
                pto = math.log((1 - self._lambda) * fptd + self._lambda * ptc) * ftq
                pqo[object_id] = pqo.get(object_id, 0) + pto

        return RetrievalResults(pqo)

