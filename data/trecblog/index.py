# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 11:09:30 2016

@author: sure
"""

import gzip
import os
import re
from bs4 import BeautifulSoup
from Elastic import Elastic

    
def parse_and_index(index_name):
    
    elastic = Elastic(index_name)

    mappings = {
        # "id": Elastic.notanalyzed_field(),
        "title": Elastic.analyzed_field(),
        "content": Elastic.analyzed_field()
    }
    
    elastic.create_index(mappings=mappings, force=True)
    
    maindir = "/data/collections/Blogs06"
    
    # list directories
    stage1 = '20051230'
    stage2 = '20060129'
    for d in sorted(os.listdir(maindir)):
        if not d.startswith("200"):
            continue
        dirname = os.path.join(maindir, d)
        ## stage1: Index first 24 directories by removing the next three "#"
        if dirname[-8:] > stage1:
            continue
        print(dirname,int(dirname[-8:]))
        
        # stage2: Index the middle 24 directories by removing the next three "#"
        #if dirname[-8:] <= stage1 or dirname[-8:]>stage2:
         #   continue
        #print(dirname,int(dirname[-8:]))
        
        # stage3: Index the last 23 directories by removing the next three #
        #if dirname[-8:] <= stage2:
            #continue
        #print(dirname,int(dirname[-8:]))

        for f in os.listdir(dirname):
            if f.startswith("permalinks-"):
                inpath = os.path.join(dirname, f)
                print(inpath)
    
                infile = gzip.GzipFile(inpath, "r")
                isParse = False
                docs = {}
                for line in infile:
                    charset = "utf-8"
                    line = line.lower().decode(charset)#bytes to string
                    if ("<docno>") in line: # get doc id
                        docno = re.sub(("<docno>|</docno>|\n"),"",line.strip(" "))
                
                    elif ("charset") in line and (">") not in line:  #encode method             
                        charset = line[33:]
                
                    elif ("</dochdr>") in line: # start to parse
                        isParse = True
                        doc_dict = {}
                        doc = ""
                
                    elif ("</doc>") in line: # finish parse
                        isParse = False
                        try:
                            soup = BeautifulSoup(doc,'lxml')
                            try:
                                title = soup.title.text
                            except: # if there is no title, use an empty string instead
                                title = ""
                            [script.extract() for script in soup.findAll('script')]
                            [style.extract() for style in soup.findAll('style')]
                            soup.prettify()
                            reg1 = re.compile("<[^>]*>")
                            content = reg1.sub('',soup.prettify())
                            doc_dict["title"] = title
                            doc_dict["content"] = content
                            docs[docno] = doc_dict               
                            #print (docno)
                            #print (content)
                        except:
                            # files beautifulsoup can not handle
                            title = ""
                            content = doc
                            doc_dict["title"] = title
                            doc_dict["content"] = content                    
                            docs[docno] = doc_dict                            
                    
                    elif isParse:
                        # parse doc
                        doc += line
                
                "continous update docs and add into index"
                elastic.add_docs_bulk(docs)
                print ("finish parse and index for file: ",inpath)

              
if __name__ == "__main__":
    index_name = "blogs06"
    parse_and_index(index_name)
            
                
        
