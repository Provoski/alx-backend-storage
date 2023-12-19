#!/usr/bin/env python3
'''11-schools_by_topic'''


def schools_by_topic(mongo_collection, topic):
    '''
    schools_by_topic - returns the list of school having a specific topic
    args:
        mongo_collection - pymongo collection object
        topic -  topic searched
    return - list of school
    '''
    query = {'topic': topic}
    result = mongo_collection.find(query) 
    return result
