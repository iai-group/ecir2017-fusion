from scipy.stats import ttest_rel

if __name__ == "__main__":
    runfile1 = "output/results/blog07/ebm25_blog07_1.txt"
    runfile2 = "output/results/blog07/ebm25_blog07_2.txt"
    map_list1 = []
    map_list2 = []
    f1 = open(runfile1, "r")
    for line in f1:
        metric, query_id, score = line.split()
        if metric == "map":
            map_list1.append(float(score))
    f2 = open(runfile2, "r")
    for line in f2:
        metric, query_id, score = line.split()
        if metric == "map":
            map_list2.append(float(score))
    res = ttest_rel(map_list1, map_list2)
    print(type(res))
    print(res)
