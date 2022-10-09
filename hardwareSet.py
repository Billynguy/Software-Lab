import connector
from datetime import datetime


class HWSet:
    # Constructor
    def __init__(self, name, qty):
        c = connector.Connector("HWSet")
        document = {
            'name': name,
            'capacity': qty,
            'availability': qty,
            'projects': {"100": 0, "101": 0},
            'updated': datetime.now()
        }
        c.collection.insert_one(document)
        c.terminate()
        return

    # Getters
    @staticmethod
    def get_names():
        c = connector.Connector("HWSet")
        names = []
        for x in c.collection.find({}, {"_id": 0, "name": 1}):
            names.append(x.get('name'))
        c.terminate()
        return names

    @staticmethod
    def get_capacity(hwset):
        c = connector.Connector("HWSet")
        capacity = c.collection.find_one({'name': hwset}, {'_id': 0, 'capacity': 1})
        c.terminate()
        return capacity.get('capacity')

    @staticmethod
    def get_availability(hwset):
        c = connector.Connector("HWSet")
        availability = c.collection.find_one({'name': hwset}, {'_id': 0, 'availability': 1})
        c.terminate()
        return availability.get('availability')

    @staticmethod
    def get_checkedout_list(hwset):
        c = connector.Connector("HWSet")
        projects = c.collection.find_one({'name': hwset}, {'_id': 0, 'projects': 1})
        c.terminate()
        return projects.get('projects')

    # NEED TO FINISH!
    # Checks out resources
    @staticmethod
    def check_out(hwset, pid, amount):
        # Checks if qty is > availability, if so deny the transaction
        capacity = HWSet.get_capacity(hwset)
        availability = HWSet.get_availability(hwset)
        if amount > availability:
            print("Too much! Do less!")
            return -1
        # There is availability! Give it to them
        else:
            availability -= amount
            c = connector.Connector("HWSet")
            myquery = {"name": hwset}
            newvalues = {"$set": {"availability": availability, "updated": datetime.now()}}
            c.collection.update_one(myquery, newvalues)
            projects = HWSet.get_checkedout_list()
            # for x in projects:
            #     if x == pid:


        return

    # NEED TO FINISH!
    @staticmethod
    # Checks in resources
    def check_in(hwset, pid, qty):
        # No error checking needed but maybe need to check if too much is given where capacity < availability

        return
