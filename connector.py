from pymongo import MongoClient

# Used to connect to database
class Connector:
    def __init__(self, database):
        self.client = MongoClient("mongodb+srv://lphadmin:<password>@lph.m8yzz0g.mongodb.net/?retryWrites=true&w=majority")
        db = self.client['Cluster0']
        self.collection = db[database]

    def terminate(self):
        self.client.close
        return
