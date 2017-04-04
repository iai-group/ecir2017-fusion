"""Abstract class for fusion-based scoring.

@author: Shuo Zhang
@author: Krisztian Balog
"""
import operator


class FusionScorer(object):
    ASSOC_MODE_BINARY = 1
    ASSOC_MODE_UNIFORM = 2

    """Abstract class for any fusion-based method."""

    def __init__(self, index_name, association_file, run_id="fusion"):
        """
        :param index_name: name of index
        :param association_file: association file
        """
        self._index_name = index_name
        self.association_file = association_file
        self.assoc_obj = {}
        self.assoc_doc = {}
        self.run_id = run_id

    def load_associations(self):
        """Loads the document-object associations."""
        # file format: documentId objectId per line
        f = open(self.association_file)
        for line in f:
            doc_id, object_id = line.split()
            if object_id not in self.assoc_obj.keys():
                self.assoc_obj[object_id] = []
            self.assoc_obj[object_id].append(doc_id)
            if doc_id not in self.assoc_doc.keys():
                self.assoc_doc[doc_id] = []
            self.assoc_doc[doc_id].append(object_id)

    def score_query(self, query):
        pass

    def score_queries(self, queries, output_file):
        """Scores all queries and optionally dumps results into an output file."""
        out = open(output_file, "w")
        for query_id in sorted(queries):
            query = queries[query_id]
            pqo = self.score_query(query)
            self.write_trec_format(pqo, query_id, self.run_id, out)
        out.close()

    def write_trec_format(self, pqo, query_id, run_id, out, max_rank=100):
        """Outputs results in TREC format"""
        rank = 1
        for doc_id, score in self.get_scores_sorted(pqo):
            if rank <= max_rank:
                out.write(query_id + "\tQ0\t" + doc_id + "\t" + str(rank) + "\t" + str(score) + "\t" + run_id + "\n")
            rank += 1

    def get_scores_sorted(self, pqo):
        """Returns all results sorted by score"""
        return sorted(pqo.items(), key=operator.itemgetter(1), reverse=True)

    def load_queries(self, query_file):
        """Loads the query file
        :return: query dictionary {queryID:query([term1,term2,...])}
        """
        f = open(query_file, "r")
        queries = {}
        for line in f:
            tmp = line.split()
            query_id = tmp[0]
            query = tmp[1:]
            queries[query_id] = query
        f.close()
        return queries

    def parse(self, text):
        stopwords = [
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in",
            "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the",
            "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"]
        terms = []
        # Replace specific characters with space
        chars = ["'", ".", ":", ",", "/", "(", ")", "-", "+"]
        for ch in chars:
            if ch in text:
                text = text.replace(ch, " ")
        # Tokenization
        for term in text.split():  # default behavior of the split is to split on one or more whitespaces
            # Lowercasing
            term = term.lower()
            # Stopword removal
            if term in stopwords:
                continue
            terms.append(term)
        return terms
