from nordlys.logic.fusion.fusion_scorer_early_bm25 import EarlyFusionScorer

if __name__ == "__main__":
    index_name = "blogs06"
    assoc_file = "data/trecblog/assoc_blog06.txt"
    object_length_file = "data/trecblog/ol_blog06.txt"
    assoc_mode = 1
    retr_params = {"k1":1.2, "b":0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode, retr_params, num=3000)
    ef.load_associations()
    query_file = "data/trecblog/query_blog07.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/blog07/ebm25_blog07_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "blogs06"
    assoc_file = "data/trecblog/assoc_blog06.txt"
    assoc_mode1 = 2
    retr_params = {"k1":1.2, "b":0.75}
    ef = EarlyFusionScorer(index_name, assoc_file, object_length_file, assoc_mode1, retr_params, num=3000)
    ef.load_associations()
    query_file = "data/trecblog/query_blog07.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/blog07/ebm25_blog07_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
