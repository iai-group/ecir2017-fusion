from nordlys.logic.fusion.fusion_scorer_late import LateFusionScorer

if __name__ == "__main__":
    index_name = "fedweb14"
    assoc_file = "data/trecfed/assoc_fed14.txt"
    assoc_mode = 1
    retr_mode = "LMJelinekMercer"
    retr_params = {"lambda": 0.1}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode, retr_mode, retr_params, num = 10000)
    ef.load_associations()
    query_file = "data/trecfed/query_2014.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/fed14/llm_fed14_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "fedweb14"
    assoc_file = "data/trecfed/assoc_fed14.txt"
    assoc_mode1 = 2
    retr_mode = "LMJelinekMercer"
    retr_params = {"lambda": 0.1}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode1, retr_mode, retr_params, num = 10000)
    ef.load_associations()
    query_file = "data/trecfed/query_2014.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/fed14/llm_fed14_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
