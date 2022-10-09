import connector
from datetime import datetime


class Projects:

    # Constructor
    # Project ID will be server-generated.
    # Project name, description will be provided by the creator.
    # Admin will automatically be the user who created it, need to be checked with user class
    # users and hwsets are initialized to empty lists since they'll be constantly modified
    def __init__(self, pid, name, description, admin):
        c = connector.Connector("Projects")
        document1 = {
            'creation': datetime.now(),
            'id': pid,
            'name': name,
            'description': description,
            'admin': admin,
            'users': [admin],
            'hwsets': [],
            'updated': datetime.now()
        }
        c.collection.insert_one(document1)
        c.terminate()
        return

    # Getters
    @staticmethod
    def get_name(pid):
        c = connector.Connector("Projects")
        name = c.collection.find_one({'id': pid}, {'_id':0, 'name': 1})
        c.terminate()
        return name.get('name')

    @staticmethod
    def get_description(pid):
        c = connector.Connector("Projects")
        desc = c.collection.find_one({'id': pid}, {'_id': 0, 'description': 1})
        c.terminate()
        return desc.get('description')

    @staticmethod
    def get_users(pid):
        c = connector.Connector("Projects")
        users = c.collection.find_one({'id': pid}, {'_id': 0, 'users': 1})
        c.terminate()
        return users.get('users')

    @staticmethod
    def get_hwsets(pid):
        c = connector.Connector("Projects")
        hwsets = c.collection.find_one({'id': pid}, {'_id': 0, 'hwsets': 1})
        c.terminate()
        return hwsets.get('hwsets')

    # User configuration

    @staticmethod
    def add_user(pid, user):
        users = Projects.get_users(pid)
        for x in users:
            if x == user:
                return
            else:
                continue
        users.append(user)
        c = connector.Connector("Projects")
        myquery = {"id": pid}
        newvalues = {"$set": {"users": users, "updated": datetime.now()}}
        c.collection.update_one(myquery, newvalues)
        c.terminate()

    @staticmethod
    def remove_user(pid, user):
        users = Projects.get_users(pid)
        try:
            users.remove(user)
            c = connector.Connector("Projects")
            myquery = {"id": pid}
            newvalues = {"$set": {"users": users, "updated": datetime.now()}}
            c.collection.update_one(myquery, newvalues)
            c.terminate()
            return
        except ValueError:
            print("User not found")
            return -1

    # HWSets configuration
    @staticmethod
    def add_hwsets(pid, hw):
        hwsets = Projects.get_hwsets(pid)
        for x in hwsets:
            if x == hw:
                return
            else:
                continue
        hwsets.append(hw)
        c = connector.Connector("Projects")
        myquery = {"id": pid}
        newvalues = {"$set": {"hwsets": hwsets, "updated": datetime.now()}}
        c.collection.update_one(myquery, newvalues)
        c.terminate()
        return

    @staticmethod
    def remove_hwsets(pid, hw):
        hwsets = Projects.get_hwsets(pid)
        try:
            hwsets.remove(hw)
            c = connector.Connector("Projects")
            myquery = {"id": pid}
            newvalues = {"$set": {"hwsets": hwsets, "updated": datetime.now()}}
            c.collection.update_one(myquery, newvalues)
            c.terminate()
            return
        except ValueError:
            print("HWSet not found")
            return -1
