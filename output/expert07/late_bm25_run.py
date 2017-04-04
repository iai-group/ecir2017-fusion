from nordlys.logic.fusion.fusion_scorer_late import LateFusionScorer

if __name__ == "__main__":
    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode = 1
    retr_mode = "BM25"
    retr_params = {"k1":1.2, "b":0.75}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode, retr_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2007.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert07/lbm25_ex07_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode1 = 2
    retr_mode = "BM25"
    retr_params = {"k1":1.2, "b":0.75}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode1, retr_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2007.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert07/lbm25_ex07_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
