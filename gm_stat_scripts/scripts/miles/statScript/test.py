#!/usr/local/bin/python

import pymongo

def test_new_mongodb_driver():
    connection = pymongo.MongoClient(host='mongodb://172.16.0.211:27017,172.16.0.212:27017/tracker_db', safe=True,  read_preference=pymongo.ReadPreference.SECONDARY)

    connection.admin.authenticate('reader', 'rr1ee2aa3dd4')

    tracker_db = connection.tracker_db
    logs = tracker_db.logs

    for u in logs.find().limit(5):
        print u
    connection.close()


if __name__ == '__main__':
    test_new_mongodb_driver()


