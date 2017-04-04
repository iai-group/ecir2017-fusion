from nordlys.logic.fusion.fusion_scorer import FusionScorer
from nordlys.core.retrieval.elastic import Elastic

if __name__ == "__main__":
    index_name = "cerc-expert"
    assoc_file = "data/trecent/assoc_cerc.txt"
    ef = FusionScorer(index_name, assoc_file)
    ef.load_associations()
    elastic = Elastic(index_name)
    outputfile = "output/ol_expert07.txt"
    f = open(outputfile, "w")
    for object_id, doc_ids in ef.assoc_obj.items():
        length = 0
        for doc_id in doc_ids:
            print(doc_id)
            try:
                length += elastic.doc_length(doc_id, "content")
            except:
                length += 0
        f.write(object_id + "\t" + str(length) + "\n")
    f.close()

    index_name = "febweb14"
    assoc_file = "data/trecfed/assoc_feb14.txt"
    ef = FusionScorer(index_name, assoc_file)
    ef.load_associations()
    elastic = Elastic(index_name)
    outputfile = "output/ol_feb14.txt"
    f = open(outputfile, "w")
    for object_id, doc_ids in ef.assoc_obj.items():
        length = 0
        for doc_id in doc_ids:
            print(doc_id)
            try:
                length += elastic.doc_length(doc_id, "content")
            except:
                length += 0
        f.write(object_id + "\t" + str(length) + "\n")
    f.close()

    index_name = "febweb13"
    assoc_file = "data/trecfed/assoc_feb13.txt"
    ef = FusionScorer(index_name, assoc_file)
    ef.load_associations()
    elastic = Elastic(index_name)
    outputfile = "output/ol_feb13.txt"
    f = open(outputfile, "w")
    for object_id, doc_ids in ef.assoc_obj.items():
        length = 0
        for doc_id in doc_ids:
            print(doc_id)
            try:
                length += elastic.doc_length(doc_id, "content")
            except:
                length += 0
        f.write(object_id + "\t" + str(length) + "\n")
    f.close()

'''
if __name__ == "__main__":
    index_name = "blog06"
    assoc_file = "data/trecblog/assoc_blog06.txt"
    ef = FusionScorer(index_name, assoc_file)
    ef.load_associations()
    elastic = Elastic(index_name)
    outputfile = "output/ol_blog06.txt"
    f = open(outputfile, "w")
    for object_id, doc_ids in ef.assoc_obj.items():
        length = 0
        for doc_id in doc_ids:
            print(doc_id)
            try:
                length += elastic.doc_length(doc_id, "content")
            except:
                length += 0
        f.write(object_id + "\t" + str(length) + "\n")
    f.close()
    '''
