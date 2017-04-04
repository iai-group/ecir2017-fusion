"""Global nordlys config.

@author: Krisztian Balog
@author: Faegheh Hasibi
"""

import os
from nordlys.core.utils.file_utils import FileUtils


def load_nordlys_config(file_name):
    """Loads nordlys config file. If local file is provided, global one is ignored."""
    config_path = os.sep.join([BASE_DIR, "config"])
    local_config = os.sep.join([config_path, "local", file_name])
    if os.path.exists(local_config):
        return FileUtils.load_config(local_config)
    else:
        return FileUtils.load_config(os.sep.join([config_path, file_name]))


NORDLYS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.sep.join([BASE_DIR, "data"])
LIB_DIR = os.sep.join([BASE_DIR, "lib"])

# config for MongoDB
MONGO_CONFIG = load_nordlys_config("mongo.json")
MONGO_HOST = MONGO_CONFIG['host']
MONGO_DB = MONGO_CONFIG['db']
MONGO_COLLECTION_DBPEDIA = MONGO_CONFIG['collection_dbpedia']
MONGO_COLLECTION_SF_FACC = MONGO_CONFIG['collection_sf_facc']
MONGO_COLLECTION_WORD2VEC = MONGO_CONFIG['collection_word2vec']
MONGO_COLLECTION_FREEBASE2DBPEDIA = MONGO_CONFIG['collection_freebase2dbpedia']

# config for Elasticsearch
ELASTIC_CONFIG = load_nordlys_config("elastic.json")
ELASTIC_HOSTS = ELASTIC_CONFIG['hosts']
ELASTIC_SETTINGS = ELASTIC_CONFIG['settings']

# config for entity package
ENTITY_CONFIG = load_nordlys_config("entity.json")
ENTITY_COLLECTIONS = ENTITY_CONFIG['entity_collections']

# config for trec_eval
TREC_EVAL = os.sep.join([LIB_DIR, "trec_eval", "trec_eval"])