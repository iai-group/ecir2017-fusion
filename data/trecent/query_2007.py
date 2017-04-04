# -*- coding: utf-8 -*-
"""
This file is used for extracting all queries from  "07.topics.CE001-050.txt".


@author: Shuo Zhang
"""
import os
import re

def queryExtract(query_file):
    """
    : query_file: query file storing all queries in expert search 2007.
    """
    
    maindir = "/data/collections/cerc/trecent2007"
    dname = os.path.join(maindir, "07.topics.CE001-050.txt")
    infile = open(dname)
    f = open(query_file,"w")
    for line in infile:
        if "num" in line:
            query_id = re.sub("<num>|</num>|\n","",line.strip(" "))
        elif "query" in line:
            query = re.sub("<query>|</query>|\n","",line.strip(" "))
            line  = query_id+" "+query+"\n"
            f.write(line)

    f.close()
    infile.close()
        
if __name__ == "__main__":
    queryExtract("query_2007.txt")
    
    
