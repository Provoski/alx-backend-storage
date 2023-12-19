#!/usr/bin/env python3
'''8-all module'''


def list_all(mongo_collection):
    '''
    list_all - lists all documents in a collection
    args:
        mongo_collection - pymongo collection object
    return - empty list if no document in the collection or list of collections
    '''

    documents = list(mongo_collection.find())
    return documents if documents else []
