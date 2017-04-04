from nordlys.logic.fusion.fusion_scorer_late import LateFusionScorer

if __name__ == "__main__":
    index_name = "blogs06"
    assoc_file = "data/trecblog/assoc_blog06.txt"
    assoc_mode = 1
    retr_mode = "BM25"
    retr_params = {"k1":1.2, "b":0.75}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode, retr_mode, retr_params, num=2000)
    ef.load_associations()
    query_file = "data/trecblog/query_blog07.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/blog07/lbm25_blog07_1.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)

    index_name = "blogs06"
    assoc_file = "data/trecblog/assoc_blog06.txt"
    assoc_mode1 = 2
    retr_mode = "BM25"
    retr_params = {"k1":1.2, "b":0.75}
    ef = LateFusionScorer(index_name, assoc_file, assoc_mode1, retr_mode, retr_params, num=2000)
    ef.load_associations()
    query_file = "data/trecblog/query_blog07.txt"
    queries = ef.load_queries(query_file)
    outputfile = "output/blog07/lbm25_blog07_2.txt"
    #e:early-fusion lm:language modeling feb14:federated 14 1:binary
    ef.score_queries(queries, outputfile)
