# -*- coding: utf-8 -*-
"""
This file is used for indexing CERC data collection.

@author: Shuo Zhang
"""

import os
import re
from bs4 import BeautifulSoup
from Elastic import Elastic

def CERC_index(index_name):

    elastic = Elastic(index_name) 
    mappings = {
        # "id": Elastic.notanalyzed_field(),
        "title": Elastic.analyzed_field(),
        "content": Elastic.analyzed_field()
    }
    
    elastic.create_index(mappings=mappings, force=True)
    
    maindir = "/data/collections/cerc/csiro-corpus"
    num_doc = 0
    for d in os.listdir(maindir):
        inpath = os.path.join(maindir,d)
        infile = open(inpath,mode="r", errors="ignore")
        docs = {}
        isParse = False
        for line in infile.readlines():
            #charset = "utf-8"
            line = line.lower()
            if ("<docno>") in line: # get doc id
                docno = re.sub(("<docno>|</docno>|\n"),"",line.strip(" "))
                
            elif ("</dochdr>") in line: # start to parse
                isParse = True
                doc_dict = {}
                doc = ""
            elif ("</doc>") in line: # finish parse
                isParse = False
                try:
                    soup = BeautifulSoup(doc,"lxml")
                    try:
                        title = soup.title.text
                    except: # if there is no title, use an empty string instead
                        title = ""
                    [script.extract() for script in soup.findAll("script")]
                    [style.extract() for style in soup.findAll("style")]
                    soup.prettify()
                    reg1 = re.compile("<[^>]*>")
                    content = reg1.sub('',soup.prettify())
                    doc_dict["title"] = title
                    doc_dict["content"] = content                    
                    docs[docno] = doc_dict
                    num_doc += 1
                    
                except:
                    # other files apart from html
                    title = ""
                    content = doc
                    print (content)
                    doc_dict["title"] = title
                    doc_dict["content"] = content                    
                    docs[docno] = doc_dict 
                    num_doc += 1
                                     
            elif isParse:
                # parse doc
                doc += line
        
        "continous update docs and add into index"
        elastic.add_docs_bulk(docs)
        print ("finish parse and index for file: ",inpath)
        
    print(num_doc," documents indexed")

            
        

if __name__ == "__main__":
    CERC_index("cerc-expert")
    