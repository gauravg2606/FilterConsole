__author__ = 'hitesh'
import pymongo

__dropboxdb_inst = None

def get_dropboxstickerdb_instance():
    global __dropboxdb_inst
    if __dropboxdb_inst is None:
        __dropboxdb_inst = pymongo.MongoClient("10.0.1.13",27017).dropboxstickerdb
    return __dropboxdb_inst