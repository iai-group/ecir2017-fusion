# -*- coding: utf-8 -*-
"""
This file is used for extracting all queries from  "08.topics.CE051-127.txt".


@author: Shuo Zhang
"""
import os
import re

def queryExtract(query_file):
    """
    : query_file: query file storing all queries in expert search 2008.
    """
    
    maindir = "/data/collections/cerc/trecent2008"
    dname = os.path.join(maindir, "08.topics.CE051-127.txt")
    infile = open(dname)
    f = open(query_file,"w")
    for line in infile:
        if "num" in line:
            query_id = re.sub("<num>|</num>|\n","",line.strip(" "))
        elif "query" in line:
            query = re.sub("<query>|</query>|\n","",line.strip(" "))
            no = query_id[3:]
            if int(no) < 100:
                line  = no[1:]+" "+query+"\n"                
            else:
                line  = no+" "+query+"\n"
            f.write(line)
    f.close()
    infile.close()
        
if __name__ == "__main__":
    queryExtract("query_2008.txt")
    
    
