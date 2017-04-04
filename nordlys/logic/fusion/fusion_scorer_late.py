"""
Late fusion scorer (i.e., document-centric model).

@author: Shuo Zhang
@author: Krisztian Balog
"""
from nordlys.logic.fusion.fusion_scorer import FusionScorer
from nordlys.core.retrieval.elastic import Elastic
from nordlys.core.retrieval.retrieval_results import RetrievalResults


class LateFusionScorer(FusionScorer):
    def __init__(self, index_name, association_file, assoc_mode, retr_model, retr_params, num_docs=None,
                 field="content", run_id="fusion", num=100):
        """

        :param index_name: name of index
        :param association_file: document-object association file
        :param assoc_mode: document-object weight mode, uniform or binary
        :param retr_model: document-object weight mode, uniform or binary
        :param retr_params: parameter in similarity method
        """
        self._index_name = index_name
        self._field = field
        self._num_docs = num_docs
        self._elastic = Elastic(self._index_name)
        self._model = retr_model
        self._params = retr_params
        self._elastic.update_similarity(self._model, self._params)
        self.association_file = association_file
        self.assoc_doc = {}
        self.assoc_obj = {}
        self.run_id = run_id
        self._assoc_mode = assoc_mode
        self._num = num

    def score_query(self, query):
        """
        Scores a given query.

        :param query: query to be searched
        :return: pqo dict
        """
        # retrieving documents
        aquery = self._elastic.analyze_query(query)  # analyzed query
        res = self._elastic.search(aquery, self._field, num=self._num)

        # scoring objects, i.e., computing P(q|o)
        pqo = {}
        for i, item in enumerate(list(res.keys())):
            if self._num_docs is not None and i + 1 == self._num_docs:  # consider only top documents
                break
            doc_id = item
            doc_score = res[doc_id]
            if doc_id in self.assoc_doc:
                for object_id in self.assoc_doc[doc_id]:
                    if self._assoc_mode == FusionScorer.ASSOC_MODE_BINARY:
                        w_do = 1
                    elif self._assoc_mode == FusionScorer.ASSOC_MODE_UNIFORM:
                        w_do = 1 / len(self.assoc_obj[object_id])
                    else:
                        w_do = 0  # this should never happen
                    pqo[object_id] = pqo.get(object_id, 0) + doc_score * w_do

        return RetrievalResults(pqo)

