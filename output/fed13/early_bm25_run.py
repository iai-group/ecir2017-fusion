from nordlys.logic.fusion.fusion_scorer_early_bm25 import EarlyFusionScorer

if __name__ == "__main__":
    index_name = "fedweb13"
    assoc_file = "data/trecfed/assoc_fed13.txt"
    object_length_file = "data/trecfed/ol_fed13.txt"
    assoc_mode = 1
    retr_params = {"k1": 1.2, "b": 0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode, retr_params, num = 100)
    ef.load_associations()
    query_file = "data/trecfed/query_2013.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/fed13/ebm25_fed13_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "fedweb13"
    assoc_file = "data/trecfed/assoc_fed13.txt"
    assoc_mode1 = 2
    retr_params = {"k1": 1.2, "b": 0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode1, retr_params, num = 100)
    ef.load_associations()
    query_file = "data/trecfed/query_2013.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/fed13/ebm25_fed13_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
