#!/usr/bin/env python3
'''12-log_stats'''
from pymongo import MongoClient


def nginx_logs_stats():
    ''' output nginx method log stat '''

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    '''Get total number of logs'''
    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))
    print("Methods:")

    '''Get counts for each HTTP method'''
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, count))

    '''Get count for specific method and path'''
    specific_log_count = collection.count_documents({
        "method": "GET", "path": "/status"
        })
    print("{} status check".format(specific_log_count))


if __name__ == "__main__":
    nginx_logs_stats()
