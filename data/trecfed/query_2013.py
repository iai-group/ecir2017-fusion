# -*- coding: utf-8 -*-
"""
This file is used for extracting all queries from  "FW-topic.xml".
From "FW13-topics-evaluation-TREC", outputs all queries in 2013

@author: Shuo Zhang
"""
import os
import re

def queryExtract(query_file):
    """
    : query_file: query file storing all queries in FedWeb 2013
    """
    
    maindir = "/data/collections/fedwebgh/meta_data/topics"
    dname = os.path.join(maindir, "FW-topics.xml")
    query_all = {}
    infile = open(dname)
    for line in infile:
        if "topic evaluation" in line:
            query_id = line.split()[2][-5:-1]
        elif "query" in line:
            if "note" in line:
                continue
            query = re.sub("<query>|</query>|\n","",line.strip(" "))           
            query_all[query_id] = query
    infile.close()
    
    eqname = os.path.join(maindir, "FW13-topics-evaluation-TREC.txt")
    f = open(query_file,"w")
    file = open(eqname)
    
    for line in file:
        topic_id = line[:4]
        line = topic_id+ " "+query_all[topic_id].lower()+"\n"
        f.write(line)
    f.close()
    file.close()
        
if __name__ == "__main__":
    queryExtract("query_2013.txt")
    
    
