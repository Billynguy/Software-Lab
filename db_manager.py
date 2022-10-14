from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


# For the purposes of our Flask app, we probably only need a singleton access.
class DBManager:
    """Manager for a connection to our database system.
    In this case, MongoDB.
    """

    def __init__(self):
        """Connect to a MongoDB server and obtain collections.
        The connection should be `close`'d if directly constructed.
        """
        self.__client: MongoClient = MongoClient('mongodb+srv://lphadmin:<password>@lph.m8yzz0g.mongodb.net/?retryWrites=true&w=majority')
        self.__db: Database = self.__client['Cluster0']
        self.__users_collection: Collection = self.__db['Users']
        self.__projects_collection: Collection = self.__db['Projects']
        self.__hwsets_collection: Collection = self.__db['HWSet']

    def close(self) -> None:
        """Close the connection to the MongoDB server obtained in the constructor.
        After calling, this object should not be used anymore.
        Do not directly call if this object was used as a contextmanager.
        """
        self.__client.close()

    """These are accessor methods that expose collections.
    We should make specific accessor and modifier methods instead.
    Otherwise, client code needs to manage documents of these collections safely.
    """
    def get_users_collection(self) -> Collection:
        return self.__users_collection

    def get_projects_collection(self) -> Collection:
        return self.__projects_collection

    def get_hwsets_collection(self) -> Collection:
        return self.__hwsets_collection

    """We can use DBManager as a contextmanager,
    but we will probably only do so for one-off operations.
    """
    def __enter__(self) -> 'DBManager':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
