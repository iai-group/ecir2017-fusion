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
    
    maindir = "./data"
    dname = os.path.join(maindir, "08.blog.feeddist.topics.txt")
    infile = open(dname)
    print(infile)
    f = open(query_file,"w")
    for line in infile:
        
        if "num" in line:
            line = re.sub("<num>|</num>|\n","",line.strip(" "))
            query_id=line.split(" ")[2]            
            print(query_id)
        elif "title" in line:
            query = re.sub("<title>|</title>|\n","",line.strip(" "))
            line  = query_id+" "+query+"\n"
            print(line)
            f.write(line)

    f.close()
    infile.close()
        
if __name__ == "__main__":
    queryExtract("./query_blog08.txt")
    
    

