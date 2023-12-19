#!/usr/bin/env python3
'''9-insert_school module'''


def insert_school(mongo_collection, **kwargs):
    '''
    insert_school - inserts a new document in a collection based on kwargs
    aegs:
        mongo_collection - pymongo collection object
    return - the new _id of newly inserted document
    '''

    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
