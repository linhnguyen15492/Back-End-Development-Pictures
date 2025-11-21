from pymongo import MongoClient


def init_db():
    # client = MongoClient("mongodb://%s:%s@192.168.9.195:27017" % ("mongouser", "password"))
    client = MongoClient("mongodb://192.168.9.195:27017")
    client.tododb.todo.drop()
    client.tododb.todo.insert_many(
        [
            {"priority": "high", "title": "Get milk"},
            {"priority": "medium", "title": "Get gasoline"},
            {"priority": "low", "title": "Water plants"},
        ]
    )
    return client
