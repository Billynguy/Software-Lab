from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os

"""We have a DBManager abstract class from which the DBManagerImplementation and DBManagerMock classes override.
"""

# Load secrets from .env
load_dotenv()


class DBManagerImplementation:
    """Manager for a connection to our actual database system.
    In this case, MongoDB.
    """

    def __init__(self):
        """Connect to a MongoDB server and obtain collections.
        The connection should be `close`'d if directly constructed.
        """
        self.__client: MongoClient = MongoClient(
            f'mongodb+srv://{os.environ["MONGODB_USERNAME"]}:{os.environ["MONGODB_PASSWORD"]}'
            f'@{os.environ["MONGODB_CLUSTER_ADDRESS"]}/?retryWrites=true&w=majority'
        )
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
    """

    def __get_users_collection(self) -> Collection:
        return self.__users_collection

    def __get_projects_collection(self) -> Collection:
        return self.__projects_collection

    def __get_hwsets_collection(self) -> Collection:
        return self.__hwsets_collection

    """These accessor methods are more specific.
    """
    def insert_user_document(self, user_document: dict) -> bool:
        """Attempt to insert a user document.
        Will fail if there is an existing user document with the same userid.
        """

        if self.get_user_document_by_id(user_document['userid']) is not None:
            return False

        self.__users_collection.insert_one(user_document)
        return True

    def update_user_document(self, user_document: dict, update_element: str) -> bool:
        """Attempt to update a user's attribute
        Will fail if there is no existing user document with the same user id"""
        if self.get_user_document_by_id(user_document['userid']) is None:
            return False

        identifier = {'userid': user_document['userid']}
        update_data = {'$set': {update_element: user_document[update_element]}}
        self.__users_collection.update_one(identifier, update_data)
        return True

    def get_user_document_by_id(self, userid: str) -> Optional[dict]:
        return self.__users_collection.find_one({
            'userid': userid
        })

    def insert_project_document(self, project_document: dict) -> bool:
        """Attempt to insert a project document
        Will fail if there is an existing project with same projectid"""
        if self.get_project_document_by_id(project_document['projectid']) is not None:
            return False

        self.__projects_collection.insert_one(project_document)
        return True

    def update_project_document(self, project_document: dict, update_element: str) -> bool:
        """Attempt to update a project's attribute
        Will fail if there is no existing project document with the same project id"""
        if self.get_project_document_by_id(project_document['projectid']) is None:
            return False

        identifier = {'projectid': project_document['projectid']}
        update_data = {'$set': {update_element: project_document[update_element]}}
        self.__projects_collection.update_one(identifier, update_data)
        return True

    def get_project_document_by_id(self, projectid: str) -> Optional[dict]:
        return self.__projects_collection.find_one({
            'projectid': projectid
        })

    def insert_hwset_document(self, hwset_document: dict) -> bool:
        """Attempt to insert a HWSet document"""
        self.__hwsets_collection.insert_one(hwset_document)
        return True

    def update_hwset_document(self, hwset_document: dict, update_element: str) -> bool:
        """Attempt to update a hwset attribute
        Will fail if there is no existing hwset document with the same name"""
        if self.get_hwset_document_by_name(hwset_document['name']) is None:
            return False

        identifier = {'name': hwset_document['name']}
        update_data = {'$set': {update_element: hwset_document[update_element]}}
        self.__hwsets_collection.update_one(identifier, update_data)
        return True

    def update_hwset_document_multiple(self, hwset_document: dict, update_element1: str, update_element2: str) -> bool:
        """Attempt to update a hwset attribute
        Will fail if there is no existing hwset document with the same name"""
        if self.get_hwset_document_by_name(hwset_document['name']) is None:
            return False

        identifier = {'name': hwset_document['name']}
        update_data = {'$set': {update_element1: hwset_document[update_element1],
                                update_element2: hwset_document[update_element2]}}
        self.__hwsets_collection.update_one(identifier, update_data)
        return True

    def get_hwset_document_by_name(self, name: str) -> Optional[dict]:
        return self.__hwsets_collection.find_one({
            'name': name
        })

    def get_hwset_documents_as_generator(self) -> dict:
        """Yield each hwset document.
        """
        for hwset_doc in self.__get_hwsets_collection().find():
            yield hwset_doc

    def __enter__(self) -> 'DBManagerImplementation':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class DBManagerMock:
    """Mock class to test the interface of DBManager.
    """

    def __init__(self):
        self.__users_collection: list[dict] = []
        self.__projects_collection: list[dict] = []
        self.__hwsets_collection: list[dict] = []

    def close(self) -> None:
        """Clean up collections for new tests.
        """
        self.__users_collection.clear()
        self.__projects_collection.clear()
        self.__hwsets_collection.clear()
        pass

    def __has_userid(self, userid: str) -> bool:
        for user_doc in self.__users_collection:
            if user_doc['userid'] == userid:
                return True

        return False

    def __has_projectid(self, projectid: str) -> bool:
        for project_doc in self.__projects_collection:
            if project_doc['projectid'] == projectid:
                return True

        return False

    @staticmethod
    def __update_dict(dst: dict, src: dict):
        dst.clear()
        for key, value in src.items():
            dst[key] = value

    def insert_user_document(self, user_document: dict) -> bool:
        if self.__has_userid(user_document['userid']):
            return False

        self.__users_collection.append(user_document.copy())
        return True

    def update_user_document(self, user_document: dict, update_element: str) -> bool:
        for user_doc in self.__users_collection:
            if user_doc['userid'] == user_document['userid']:
                user_doc[update_element] = user_document[update_element]
                return True

        return False

    def get_user_document_by_id(self, userid: str) -> Optional[dict]:
        for user_doc in self.__users_collection:
            if user_doc['userid'] == userid:
                return user_doc

        return None

    def insert_project_document(self, project_document: dict) -> bool:
        if self.__has_projectid(project_document['projectid']):
            return False

        self.__projects_collection.append(project_document.copy())
        return True

    def update_project_document(self, project_document: dict, update_element: str) -> bool:
        for project_doc in self.__projects_collection:
            if project_doc['projectid'] == project_document['projectid']:
                project_doc[update_element] = project_document[update_element]
                return True

        return False

    def get_project_document_by_id(self, projectid: str) -> Optional[dict]:
        for project_doc in self.__projects_collection:
            if project_doc['projectid'] == projectid:
                return project_doc

        return None

    def insert_hwset_document(self, hwset_document: dict) -> bool:
        self.__hwsets_collection.append(hwset_document.copy())
        return True

    def update_hwset_document(self, hwset_document: dict, update_element: str) -> bool:
        for hwset_doc in self.__hwsets_collection:
            if hwset_doc['name'] == hwset_document['name']:
                hwset_doc[update_element] = hwset_document[update_element]
                return True

        return False

    def update_hwset_document_multiple(self, hwset_document: dict, update_element1: str, update_element2: str) -> bool:
        for hwset_doc in self.__hwsets_collection:
            if hwset_doc['name'] == hwset_document['name']:
                hwset_doc[update_element1] = hwset_document[update_element1]
                hwset_doc[update_element2] = hwset_document[update_element2]
                return True

        return False

    def get_hwset_document_by_name(self, name: str) -> Optional[dict]:
        for hwset_doc in self.__hwsets_collection:
            if hwset_doc['name'] == name:
                return hwset_doc

        return None

    def get_hwset_documents_as_generator(self) -> dict:
        for hwset_doc in self.__hwsets_collection:
            yield hwset_doc

    def __enter__(self) -> 'DBManagerMock':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


# For the purposes of our Flask app, we probably only need a singleton access.
class DBManager(ABC):
    """Manager for a connection to our database system.
    In this case, MongoDB.
    """

    __singleton = {
        '__underlying_class': type(DBManagerImplementation),
        '__instance': None,
    }

    @classmethod
    def get_instance(cls, underlying_class: type = DBManagerImplementation) -> 'DBManager':
        """Get the singleton instance.
        This instance should be closed only on exit.
        """

        if cls.__singleton['__instance'] is None:
            cls.__singleton['__underlying_class'] = underlying_class
            cls.__singleton['__instance'] = cls.__singleton['__underlying_class']()

        return cls.__singleton['__instance']

    @abstractmethod
    def close(self) -> None:
        """Clean up this instance.
        """
        pass

    """Accessor methods.
    """

    @abstractmethod
    def insert_user_document(self, user_document: dict) -> bool:
        """Attempt to insert a user document.
        Will fail if there is an existing user document with the same userid.
        """
        pass

    @abstractmethod
    def update_user_document(self, user_document: dict, update_element: str) -> bool:
        """Attempt to update a user's attribute
        Will fail if there is no existing user document with the same user id"""
        pass

    @abstractmethod
    def get_user_document_by_id(self, userid: str) -> Optional[dict]:
        pass

    @abstractmethod
    def insert_project_document(self, project_document: dict) -> bool:
        """Attempt to insert a project document
        Will fail if there is an existing project with same projectid"""
        pass

    @abstractmethod
    def update_project_document(self, project_document: dict, update_element: str) -> bool:
        """Attempt to update a project's attribute
        Will fail if there is no existing project document with the same project id"""
        pass

    @abstractmethod
    def get_project_document_by_id(self, projectid: str) -> Optional[dict]:
        pass

    @abstractmethod
    def insert_hwset_document(self, hwset_document: dict) -> bool:
        """Attempt to insert a HWSet document"""
        pass

    @abstractmethod
    def update_hwset_document(self, hwset_document: dict, update_element: str) -> bool:
        """Attempt to update a hwset attribute
        Will fail if there is no existing hwset document with the same name"""
        pass

    @abstractmethod
    def update_hwset_document_multiple(self, hwset_document: dict, update_element1: str, update_element2: str) -> bool:
        """Attempt to update a hwset attribute
        Will fail if there is no existing hwset document with the same name"""
        pass

    @abstractmethod
    def get_hwset_document_by_name(self, name: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_hwset_documents_as_generator(self) -> dict:
        """Yield each hwset document.
        """
        pass

    """We can use DBManager as a contextmanager,
    but we will probably only do so for one-off operations.
    """

    def __enter__(self) -> 'DBManager':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


DBManager.register(DBManagerImplementation)
DBManager.register(DBManagerMock)
