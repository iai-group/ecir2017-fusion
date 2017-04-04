from nordlys.logic.fusion.fusion_scorer_early_bm25 import EarlyFusionScorer

if __name__ == "__main__":
    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode = 1
    object_length_file = "data/trecent/ol_expert07.txt"
    retr_params = {"k1": 1.2, "b": 0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2007.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert07/ebm25_ex07_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode = 2
    retr_params = {"k1": 1.2, "b": 0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2007.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert07/ebm25_ex07_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
