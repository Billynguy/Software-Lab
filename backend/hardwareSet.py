from typing import Optional, Dict
from db_manager import DBManager
from projects import Projects


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
        self.__projects: dict[str, int] = {}
        """This is a list of projectids the hardware sets is renting out to"""

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

        hwset_doc = hwset.__pack_dict()

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
        self.__name = hwset_dict['name']
        self.__capacity = hwset_dict['capacity']
        self.__availability = hwset_dict['availability']
        self.__projects = hwset_dict['projects']

    def get_capacity(self) -> int:
        """Return the hardware set's capacity
        Returns: Capacity of hardware set
        """
        return self.__capacity

    def change_capacity(self, new_capacity: int):
        """Modifies the current capacity for whatever reason
        Returns: True if successful in changing capacity, False if failure in DBManager
        """
        self.__capacity = new_capacity
        self.__availability = new_capacity
        hwset_document = self.__pack_dict()

        if DBManager.get_instance().update_hwset_document_multiple(hwset_document, 'capacity', 'availability'):
            return True
        else:
            return False

    def get_projects(self) -> dict[str, int]:
        """Return a list of projects that is renting out from this hardware set
        This list is a copy so that client code cannot modify the internal list
        Returns: A copy of projects list
        """
        return self.__projects.copy()

    def check_out(self, projectid: str, qty: int):
        """Add/modify the project, and it's total quantity in the hardware set.
        Subtract the quantity that is being checked out with hardware set's availability.
        Add/modify the hardware set to the project's hwsets list.
        Args:
            projectid: project that is checking out
            qty: amount to be checked out
        Returns: True if there is enough availability, False if there is not enough availability, False if project doesn't exist
        """
        project = Projects.load_project(projectid)
        if project is None:
            return False

        if qty > self.__availability:
            return False

        # Everything is in-check, process the transaction!
        # Updates availability
        self.__availability -= qty

        # Updates the project
        existed = projectid in self.__projects
        if existed:
            rented = self.__projects.get(projectid) + qty
            self.__projects[projectid] = rented
        else:
            self.__projects[projectid] = qty

        updated_hwset_doc = self.__pack_dict()
        if DBManager.get_instance().update_hwset_document_multiple(updated_hwset_doc, 'availability', 'projects'):
            project.add_hwsets(self.__name, qty)
            return True
        else:
            return False

    #             myquery = {"name": hwset}
    #             newvalues = {"$set": {"projects": projects, "updated": datetime.now()}}
    #             c.collection.update_one(myquery, newvalues)
    #             newvalues = {"$inc": {"availability": -amount}}
    #             c.collection.update_one(myquery, newvalues)
    #             c.terminate()

    def check_in(self, projectid: str, qty: int):
        """Remove/modify the project, and it's total quantity in the hardware set.
        Add the quantity that is being checked in with hardware set's availability.
        Remove/modify the hardware set to the project's hwsets list.
        Args:
            projectid: project that is checking in
            qty: amount to be checked in
        Returns:
            True if availability <= capacity and resources was successfully checked in
            None if project isn't checking any resources out
            False if new availability exceeds capacity, False if project doesn't exist, False if checking in too much
        """
        project = Projects.load_project(projectid)
        if project is None:
            return False

        existed = projectid in self.__projects
        if not existed:
            return None

        if self.__projects.get(projectid) < qty:
            return False

        if self.__capacity < self.__availability + (self.__projects.get(projectid) - qty):
            return False

        # Update availability, new resources!
        self.__availability += qty

        # Update projects!
        new_rent = self.__projects.get(projectid) - qty
        if new_rent == 0:
            self.__projects.pop(projectid)
        else:
            self.__projects[projectid] = new_rent

        updated_hwset_doc = self.__pack_dict()
        if DBManager.get_instance().update_hwset_document_multiple(updated_hwset_doc, 'availability', 'projects'):
            # Update specific project!
            project.remove_hwsets(self.__name, qty)
            return True
        else:
            return False

    #                 myquery = {"name": hwset}
    #                 newvalues = {"$set": {"projects": projects, "updated": datetime.now()}}
    #                 c.collection.update_one(myquery, newvalues)
    #                 newvalues = {"$inc": {"availability": amount}}
    #                 c.collection.update_one(myquery, newvalues)
    #                 c.terminate()
    #         return True


if __name__ == '__main__':
    my_hwset = HWSet.new_hwset(name='HW123', capacity=1000)
    print(f'Created new HWSet: {my_hwset}')
    # my_hwset = HWSet.load_hwset(name='HW123')
    # print(f'Loaded an existing project: {my_hwset}')

    print("==Testing Capacity Functions==\n")
    print(f'Current Capacity: {my_hwset.get_capacity()}')
    print(f'Changing Capacity: {my_hwset.change_capacity(100)}')
    print(f'New Capacity: {my_hwset.get_capacity()}')
    print(f'Changing Capacity Back: {my_hwset.change_capacity(1000)}')
    print(f'Current Capacity: {my_hwset.get_capacity()}')

    print("\n==Testing Check-Out and Check-In Functions==\n")
    print(f'Checking Out: {my_hwset.check_out("proj123", 500)}')
    print(f'1 Project Checked Out: {my_hwset.get_projects()}')
    print(f'Checking Out: {my_hwset.check_out("proj456", 200)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking Out: {my_hwset.check_out("proj456", 200)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking Out: {my_hwset.check_out("proj456", 200)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking Out: {my_hwset.check_out("projNA", 200)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking Out: {my_hwset.check_out("proj456", 100)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')

    print(f'Checking In: {my_hwset.check_in("projNA", 250)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking In: {my_hwset.check_in("proj456", 250)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking In: {my_hwset.check_in("proj456", 500)}')
    print(f'2 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking In: {my_hwset.check_in("proj456", 250)}')
    print(f'1 Projects Checked Out: {my_hwset.get_projects()}')
    print(f'Checking In: {my_hwset.check_in("proj123", 500)}')
    print(f'0 Projects Checked Out: {my_hwset.get_projects()}')
