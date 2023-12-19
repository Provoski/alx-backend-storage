#!/usr/bin/env python3
'''10-update_topics module'''


def update_topics(mongo_collection, name, topics):
    '''
    mongo_collection - pymongo collection object
    args:
        name - school name to update
        topic - list of topics approached in the school
    return - nothing
    '''

    result = mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )
