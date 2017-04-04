from nordlys.core.retrieval.elastic import Elastic

index_name = "cerc-expert"
query = ["climate", "change"]
elas = Elastic(index_name)
model = "LMJelinekMercer"
params = {"lambda": 0.1}
elas.update_similarity(model, params)
pr = elas.search(query, "content")['hits']
print(pr[0]['_score'])
print(pr[1]['_score'])
print(pr[2]['_score'])

mode1 = "BM25"
params1 = {"k1": 1.2, "b": 0.75}
elas1 = Elastic(index_name)
elas1.update_similarity(mode1, params1)
pr1 = elas.search(query, "content")['hits']
print(pr1[0]['_score'])
print(pr1[1]['_score'])
print(pr1[2]['_score'])
