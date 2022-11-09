from typing import Optional
from db_manager import DBManager
from user import User


class Project:
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
        self.__hwsets: dict[str, int] = {}
        for hwset_doc in DBManager.get_instance().get_hwsets_collection().find():
            self.__hwsets[hwset_doc['name']] = 0
        # will get hwsets from database and set them all to 0 incase there is more than 2 or less than 2 or different names!
        """This is a dict of hwsets"""

    @staticmethod
    def new_project(projectid: str, name: str, description: str, userid: str) -> Optional['Project']:
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
        project = Project()
        project.__projectid = projectid
        project.__name = name
        project.__description = description
        project.__admin = userid
        project.__users.append(userid)

        projects_doc = project.__pack_dict()

        # Check that another project with the same projectid does not exist
        if DBManager.get_instance().insert_project_document(projects_doc):
            # Newly created project, update user's projects list!
            userOwner = User.load_user(userid)
            userOwner.add_project(projectid)
            return project

        return None

    @staticmethod
    def load_project(projectid: str) -> Optional['Project']:
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

        project_obj = Project()
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
        self.__name = project_dict['name']
        self.__description = project_dict['description']
        self.__admin = project_dict['admin']
        self.__users = project_dict['users']
        self.__hwsets = {}
        project_hwsets = project_dict['hwsets']
        for hwset_doc in DBManager.get_instance().get_hwsets_collection().find():
            hwset_name = hwset_doc['name']
            if hwset_name in project_hwsets:
                self.__hwsets[hwset_name] = project_hwsets[hwset_name]
            else:
                self.__hwsets[hwset_name] = 0

    def get_projectid(self) -> str:
        """Return the projectid of this project.
        """
        return self.__projectid

    def get_name(self) -> str:
        """Return the name of this project.
        """
        return self.__name

    def get_description(self) -> str:
        """Return the description of this project.
        """
        return self.__description

    def get_admin(self) -> str:
        """Return the userid of the admin user.
        """
        return self.__admin

    def get_users(self) -> list[str]:
        """Return a list of users that has access to the project
        This list is a copy so that client code cannot modify the internal list
        Returns: A copy of users list
        """
        return self.__users.copy()

    def add_user(self, userid: str) -> Optional[bool]:
        """Add a user from the project's authorized user list and adds the project to the user's project list
        Args:
            userid: user's id to be added
        Returns: True if user was added, None if user was already in the list, False if user being added doesn't exist, False if DBManager fails
            """
        new_user = User.load_user(userid)
        if new_user is None:
            return False

        if userid in self.__users:
            return None
        else:
            self.__users.append(userid)
            updated_project_doc = self.__pack_dict()
            if DBManager.get_instance().update_project_document(updated_project_doc, 'users'):
                new_user.add_project(self.__projectid)
                return True
            else:
                return False

    def remove_user(self, userid: str) -> Optional[bool]:
        """Remove a user from the project's authorized user list and removes the project from the user's project list
        Args:
            userid: user's id to be removed
        Returns: True if user was removed, None if user wasn't in the list, False if user being removed doesn't exist, False if DBManager fails
            """
        old_user = User.load_user(userid)
        if old_user is None:
            return False

        if userid in self.__users:
            self.__users.remove(userid)
            updated_project_doc = self.__pack_dict()
            if DBManager.get_instance().update_project_document(updated_project_doc, 'users'):
                old_user = User.load_user(userid)
                old_user.remove_project(self.__projectid)
                return True
            else:
                return False
        else:
            return None

    def has_user(self, userid: str) -> bool:
        """Check that a user is in the project's authorized user list.
        Args:
            userid: user's id to check
        Returns: True if found in list, False if not
        """
        return userid in self.__users

    def get_hwsets(self) -> dict[str, int]:
        """Return a dict of hwsets (which is a dictionary mapping name to amount) the project is renting from
        This dict is a copy so that client code cannot modify the internal dict
        Returns: A copy of hwsets dict
        """
        return self.__hwsets.copy()

    def add_hwsets(self, hwset: str, qty: int) -> bool:
        """Add a hwset and its quantity or modifies a hwset and its quantity
        Note: This method should not be called directly by the client since it does not actually modify the hwset
        Instead, the HWset object should add/modify the project's quantity and call this method on the project.
        Args:
            hwset: name of the hwset
            qty: amount being rented
        Returns: True if successful, False if failure in DBManager
            """
        existed = hwset in self.__hwsets
        if existed:
            rented = self.__hwsets.get(hwset)
            self.__hwsets[hwset] = rented + qty
        else:
            self.__hwsets[hwset] = qty

        updated_project_doc = self.__pack_dict()
        if DBManager.get_instance().update_project_document(updated_project_doc, 'hwsets'):
            return True
        else:
            return False

    def remove_hwsets(self, hwset: str, qty: int) -> Optional[bool]:
        """Remove a hwset and its quantity or modifies a hwset and its quantity
        Note: This method should not be called directly by the client since it does not actually modify the hwset
        Instead, the HWset object should remove/modify the project's quantity and call this method on the project.
        Args:
            hwset: name of the hwset
            qty: amount being rented
        Returns: True if successful, None if hardware set isn't in project, False if subtracting too much or DBManager fails
            """
        existed = hwset in self.__hwsets
        if not existed:
            return None
        else:
            rented = self.__hwsets.get(hwset)
            if rented < qty:
                return False
            else:
                new_rented = rented - qty
                if new_rented == 0:
                    self.__hwsets[hwset] = 0
                else:
                    self.__hwsets[hwset] = new_rented

        updated_project_doc = self.__pack_dict()
        if DBManager.get_instance().update_project_document(updated_project_doc, 'hwsets'):
            return True
        else:
            return False


if __name__ == '__main__':
    # my_project = Projects.new_project(projectid='proj456', name='Project 2', description='This is my second test project', userid='jb123')
    # print(f'Created new Project: {my_project}')
    my_project = Project.load_project("proj123")
    print(f'Loaded an existing project: {my_project}')

    print("==Testing User Functions==\n")
    print(f'One user: {my_project.get_users()}')
    print(f'Adding a user: {my_project.add_user("bn123")}')
    print(f'Two users: {my_project.get_users()}')
    print(f'Adding same user: {my_project.add_user("bn123")}')
    print(f'Two users: {my_project.get_users()}')
    print(f'Removing a user: {my_project.remove_user("bn123")}')
    print(f'One user: {my_project.get_users()}')
    print(f'Removing same user: {my_project.remove_user("bn123")}')
    print(f'One user: {my_project.get_users()}')

    print("\n==Testing Hardware Set Functions==\n")
    print(f'No hardware sets: {my_project.get_hwsets()}')
    print(f'Adding hardware set: {my_project.add_hwsets("HWSet123", 500)}')
    print(f'One hardware sets: {my_project.get_hwsets()}')
    print(f'Adding to same hardware set: {my_project.add_hwsets("HWSet123", 250)}')
    print(f'One hardware sets: {my_project.get_hwsets()}')
    print(f'Adding hardware set: {my_project.add_hwsets("HWSet456", 500)}')
    print(f'Two hardware sets: {my_project.get_hwsets()}')
    print(f'Removing amount from hardware set: {my_project.remove_hwsets("HWSet456", 250)}')
    print(f'Two hardware sets: {my_project.get_hwsets()}')
    print(f'Removing hardware set: {my_project.remove_hwsets("HWSet456", 250)}')
    print(f'One hardware sets: {my_project.get_hwsets()}')
    print(f'Removing same hardware set: {my_project.remove_hwsets("HWSet456", 250)}')
    print(f'One hardware sets: {my_project.get_hwsets()}')
    print(f'Removing hardware set: {my_project.remove_hwsets("HWSet123", 750)}')
    print(f'One hardware sets: {my_project.get_hwsets()}')

    # try:
    #     my_project_again = Projects.load_project("proj123")
    # except NotImplementedError as e:
    #     pass
