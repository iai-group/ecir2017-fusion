"""
This file is used to extract association for Blog06

@author: sure
"""

import gzip
import os


def extract_association(output_file):
    maindir = "/data/collections/Blogs06"
    f = open(output_file, "w")
    for d in os.listdir(maindir):
        if not d.startswith("200"):
            continue
        dirname = os.path.join(maindir, d)
        inpath = os.path.join(dirname, "permalinks.txt.gz")
        print(inpath)
        infile = gzip.GzipFile(inpath, "r")
        for line in infile:
            line = line.lower().decode('utf-8')
            blog = line.split(" ")[1]
            if blog[7:11] == "feed":
                key = blog
            elif blog[7:11] == "blog":
                pass
            else:
                line = blog + " " + key + "\n"
                f.write(line)
    f.close()


if __name__ == "__main__":
    output_file = "assoc_blog06.txt"
    extract_association(output_file)
