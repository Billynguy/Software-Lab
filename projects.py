from typing import Optional
from db_manager import DBManager


class Projects:
    """Back-end representation of projects
    A Project object can go out of sync especially in concurrent situations.
    Therefore, the object should be used only temporarily.
    """

    def __init__(self):
        """Client code should NOT directly call the constructor.
        Rather, client code should prefer the static 'new_project' and 'load_project' methods.
        """
        self.__projectid: str = ''
        self.__name: str = ''
        self.__description: str = ''
        self.__admin: str = ''
        self.__users: list[str] = []
        self.__hwsets: list[dict] = []
        """This is a list of hwsets"""

    @staticmethod
    def new_project(projectid: str, name: str, description: str, userid: str) -> Optional['Projects']:
        """Create and return a new project with the given parameters.
        Client code should use this static method instead of calling the constructor when creating a new project.
        Fails if another project with the same project id exists.
        Args:
            projectid: ID of the project
            name: name of the project
            description: description of the project
            userid: userid of the user creating it
        Returns: Project object representing the newly created project, None if another project with the same project id exists
        """
        project = Projects()
        project.__projectid = projectid
        project.__name = name
        project.__description = description
        project.__admin = userid
        project.__users.append(userid)

        projects_doc = project.__pack_dict()

        # Check that another project with the same projectid does not exist
        if DBManager.get_instance().insert_project_document(projects_doc):
            return project

        return None

    @staticmethod
    def load_project(projectid: str) -> Optional['Projects']:
        """Load a Project object from its project id.
        Client code should use this static method instead of calling the constructor when loading a project.
        Fails if there is no project with the project id.
        Args:
            projectid: Project id of the project to load
        Returns: Project object represented by the project id, None if no such project exists
        """
        project_doc = DBManager.get_instance().get_project_document_by_id(projectid)
        if project_doc is None:
            return None

        project_obj = Projects()
        project_obj.__unpack_dict(project_doc)
        return project_obj

    def __pack_dict(self) -> dict:
        """Form a dict to insert into the database.
        """
        return {
            'projectid': self.__projectid,
            'name': self.__name,
            'description': self.__description,
            'admin': self.__admin,
            'users': self.__users,
            'hwsets': self.__hwsets
        }

    def __unpack_dict(self, project_dict) -> None:
        """Retrieve information from a dict stored in the database.
        """
        self.__projectid = project_dict['projectid']
        self.__name: project_dict['name']
        self.__description: project_dict['description']
        self.__admin: project_dict['admin']
        self.__users: project_dict['users']
        self.__hwsets: project_dict['hwsets']


    def get_users(self) -> list[str]:
        """Return a list of users that has access to the project
        This list is a copy so that client code cannot modify the internal list
        Returns: A copy of users list
        """
        return self.__users.copy()

    def add_user(self, userid: str) -> bool:
        """Add a user from the project's authorized user list and adds the project to the user's project list
        Args:
            userid: user's id to be added
        Returns: True if user was added/was already in the list
            """
        if userid in self.__users:
            return True
        else:
            self.__users.append(userid)
            return True
            """*Add project to the specific user now! Or verify*"""

    def remove_user(self, userid: str) -> bool:
        """Remove a user from the project's authorized user list and removes the project from the user's project list
        Args:
            userid: user's id to be removed
        Returns: True if user was removed/wasn't in the list
            """
        if userid in self.__users:
            self.__users.remove(userid)
            """*Remove project to the specific user now! Or verify*"""
            return True
        else:
            return True

    def get_hwsets(self) -> list[dict]:
        """Return a list of hwsets (which is a dictionary since name, amount) the project is renting from
        This list is a copy so that client code cannot modify the internal list
        Returns: A copy of hwsets list
        """
        return self.__hwsets.copy()

    def _add_hwsets(self, hwset: str, qty: int) -> bool:
        """Add a hwset and its quantity or modifies a hwset and its quantity
        Note: This method should not be called directly by the client since it does not actually modify the hwset
        Instead, the HWset object should add/modify the project's quantity and call this method on the project.
        Args:
            hwset: name of the hwset
            qty: amount being rented
        Returns: True if successful, False otherwise
            """
        pass
    #         hwsets = Projects.get_hwsets(pid)
    #         for x in hwsets:
    #             if x == hw:
    #                 return
    #             else:
    #                 continue
    #         hwsets.append(hw)
    #         c = connector.Connector("Projects")
    #         myquery = {"id": pid}
    #         newvalues = {"$set": {"hwsets": hwsets, "updated": datetime.now()}}
    #         c.collection.update_one(myquery, newvalues)
    #         c.terminate()
    #         return

    def _remove_hwsets(self, hwset: str, qty: int) -> bool:
        """Remove a hwset and its quantity or modifies a hwset and its quantity
        Note: This method should not be called directly by the client since it does not actually modify the hwset
        Instead, the HWset object should remove/modify the project's quantity and call this method on the project.
        Args:
            hwset: name of the hwset
            qty: amount being rented
        Returns: True if successful, False otherwise
            """
        pass
    #         hwsets = Projects.get_hwsets(pid)
    #         try:
    #             hwsets.remove(hw)
    #             c = connector.Connector("Projects")
    #             myquery = {"id": pid}
    #             newvalues = {"$set": {"hwsets": hwsets, "updated": datetime.now()}}
    #             c.collection.update_one(myquery, newvalues)
    #             c.terminate()
    #             return
    #         except ValueError:
    #             print("HWSet not found")
    #             return -1