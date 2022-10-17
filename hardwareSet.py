from typing import Optional
from db_manager import DBManager


class HWSet:
    """Back-end representation of hardware sets
    A Hardware Set object can go out of sync especially in concurrent situations.
    Therefore, the object should be used only temporarily.
    """

    def __init__(self):
        """Client code should NOT directly call the constructor.
        Rather, client code should prefer the static 'new_project' and 'load_project' methods.
        """
        self.__name: str = ''
        self.__capacity: int = ''
        self.__availability: int = ''
        self.__projects: list[dict] = []
        """This is a list of projects the hardware sets is renting out to"""

    @staticmethod
    def new_hwset(name: str, capacity: int) -> Optional['HWSets']:
        """Create and return a new hardware set with the given parameters.
        Client code should use this static method instead of calling the constructor when creating a new hardware set.
        Fails if another hardware set with the same name exists.
        Args:
            name: name of the hardware set
            capacity: max amount a hardware set can hold
        Returns: HWSet object representing the newly created set, None if another HWSet with the same name exists
        """
        hwset = HWSet()
        hwset.__name = name
        hwset.__capacity = capacity
        hwset.__availability = capacity

        hwset_doc = hwset.__packdict()

        # Check that another hwset with the same hwset does not exist
        if DBManager.get_instance().insert_hwset_document(hwset_doc):
            return hwset

        return None

    @staticmethod
    def load_hwset(name: str) -> Optional['HWSet']:
        """Load a HWSet object from its name.
        Client code should use this static method instead of calling the constructor when loading a hwset.
        Fails if there is hwset with the name.
        Args:
            name: name of the hwset to load
        Returns: HWSet object represented by the name, None if no such hwset exists
        """
        hwset_doc = DBManager.get_instance().get_hwset_document_by_name(name)
        if hwset_doc is None:
            return None

        hwset_obj = HWSet()
        hwset_obj.__unpack_dict(hwset_doc)
        return hwset_obj

    def __pack_dict(self) -> dict:
        """Form a dict to insert into the database.
        """
        return {
            'name': self.__name,
            'capacity': self.__capacity,
            'availability': self.__availability,
            'projects': self.__projects
        }

    def __unpack_dict(self, hwset_dict) -> None:
        """Retrieve information from a dict stored in the database.
        """
        self.__name: hwset_dict['name']
        self.__capacity: hwset_dict['capacity']
        self.__availability: hwset_dict['availability']
        self.__projects: hwset_dict['projects']

    def get_projects(self) -> list[dict]:
        """Return a list of projects that is renting out from this hardware set
        This list is a copy so that client code cannot modify the internal list
        Returns: A copy of projects list
        """
        return self.__projects.copy()

    def check_out(self, projectid: str, quantity: int):
        """Add/modify the project, and it's total quantity in the hardware set.
        Subtract the quantity that is being checked out with hardware set's availability.
        Add/modify the hardware set to the project's hwsets list.
        Args:
            projectid: project that is checking out
            quantity: amount to be checked out
        Returns: True if there is enough availability, False if there is not enough availability
        """
        pass
    #         # Checks if qty is > availability, if so deny the transaction
    #         availability = HWSet.get_availability(hwset)
    #         if amount > availability:
    #             print("Too much! Do less!")
    #             return False
    #         # There is availability! Give it to them
    #         else:
    #             projects = HWSet.get_checkedout_list(hwset)
    #             for x in projects:
    #                 if x == pid:
    #                     to_rent = amount + projects.get(pid)
    #                     break
    #             else:
    #                 to_rent = amount
    #             projects[pid] = to_rent
    #             c = connector.Connector("HWSet")
    #             myquery = {"name": hwset}
    #             newvalues = {"$set": {"projects": projects, "updated": datetime.now()}}
    #             c.collection.update_one(myquery, newvalues)
    #             newvalues = {"$inc": {"availability": -amount}}
    #             c.collection.update_one(myquery, newvalues)
    #             c.terminate()
    #             return True

    def check_in(self, projectid: str, quantity: int):
        """Remove/modify the project, and it's total quantity in the hardware set.
        Add the quantity that is being checked in with hardware set's availability.
        Remove/modify the hardware set to the project's hwsets list.
        Args:
            projectid: project that is checking in
            quantity: amount to be checked in
        Returns: True if availability <= capacity and resources was successfully checked in, False otherwise
        """
        pass
    #         capacity = HWSet.get_capacity(hwset)
    #         availability = HWSet.get_availability(hwset)
    #         projects = HWSet.get_checkedout_list(hwset)
    #         for x in projects:
    #             if x == pid:
    #                 rented = projects.get(pid)
    #                 break
    #         else:
    #             print("NOT FOUND")
    #             return False
    #         if amount > rented:
    #             print("TOO MUCH, YOU HAVE LESS!")
    #             return False
    #         else:
    #             availability += amount
    #             if availability > capacity:
    #                 print("AVAILABILITY EXCEEDED CAPACITY!")
    #                 return False
    #             else:
    #                 projects[pid] = rented-amount
    #                 c = connector.Connector("HWSet")
    #                 myquery = {"name": hwset}
    #                 newvalues = {"$set": {"projects": projects, "updated": datetime.now()}}
    #                 c.collection.update_one(myquery, newvalues)
    #                 newvalues = {"$inc": {"availability": amount}}
    #                 c.collection.update_one(myquery, newvalues)
    #                 c.terminate()
    #         return True
