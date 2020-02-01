# Fusion-Based Object Retrieval
This repository provides resources developed within the following paper:

> S. Zhang and K. Balog. Design Patterns for Fusion-Based Object Retrieval. In ECIR'17, April 2017.

This study is an effort aimed at reproducing the result presented in the Fusion-Based Object paper.

This repository is structured as follows:

- config/: config files to index data(Using Elastic, ip:port number would change individually)
- nordlys/: code required for runnning fusion models
- data/: elastic index, query and evaluation files for blog distillatioin(./trecblog/), expert serach(./trecent/) and vertical search(./trecfed/)
- lib/trec_eval/: TREC evaluation file
- output/:  all run files scripts and their result files

## Data
The data we used are public data sets:
- CSIRO: The dataset was used for TREC task of expert search task in 2006 and 2007.
- Blogs06: The dataset was used for TREC task of blog distillation in 2006 and 2007, which is not for free yet.
- FedWeb13 and FedWeb14: These datasets were used for TREC task of federated search in 2013 and 2014.

## Runs
All the run files can be found in /output. E.g,
```
python -m output.blog07.early_bm25_run 
```

executes the run of early fusion model incorporating BM25 methods for blog distillation task of 2007.

## Qrels
The qrel files are all provided in data/ sub-folders.

## Citation
```
@inproceedings{Zhang:2017:DPF,
    author = {Shuo Zhang and Krisztian Balog},
    title = {Design Patterns for Fusion-Based Object Retrieval},
    booktitle = {Proceedings of the 39th European conference on Advances in Information Retrieval},
    series = {ECIR '17},
    publisher = {Springer},
    pages = {684--690},
	  year = {2017}
}
```

## Contact
If you have any question, please contact Shuo Zhang at imsure318@gmail.com.


 
