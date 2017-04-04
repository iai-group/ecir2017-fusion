from nordlys.logic.fusion.fusion_scorer_early_lm import EarlyFusionScorer

if __name__ == "__main__":
    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode = 1
    retr_params = {"lambda": 0.1}
    ef = EarlyFusionScorer(index_name, assoc_file, assoc_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2008.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert08/elm_ex08_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    assoc_mode = 2
    retr_params = {"lambda": 0.1}
    ef = EarlyFusionScorer(index_name, assoc_file, assoc_mode, retr_params)
    ef.load_associations()
    query_file = "data/trecent/query_2008.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/expert08/elm_ex08_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
