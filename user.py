from typing import Optional
from db_manager import DBManager


class User:
    """Back-end representation of a user.
    A User object can go out of sync especially in concurrent situations.
    Therefore, the object should be used only temporarily.
    """

    def __init__(self):
        """Client code should not directly call the constructor.
        Rather, client code should prefer the static `new_user` and `load_user` methods.
        """
        self.__username: str = ''
        self.__userid: str = ''
        self.__password: str = ''
        self.__projects: list[str] = []
        """This is a list of project ids."""

    @staticmethod
    def new_user(username: str, userid: str, password: str) -> Optional['User']:
        """Create and return a new user with the given parameters.
        Client code should use this static method instead of calling the constructor when creating a new user.
        Fails if another user with the same user id exists.

        Args:
            username: Username of the user
            userid: User id of the user
            password: Password of the user

        Returns: User object representing the newly created user, None if another user with the same user id exists

        """

        user = User()
        user._username = username
        user._userid = userid
        user._password = password

        user_doc = user.__pack_dict()

        # Check that another user with the same userid does not exist
        if DBManager.get_instance().insert_user_document(user_doc):
            return user

        return None

    @staticmethod
    def load_user(userid: str) -> Optional['User']:
        """Load a User object from its user id.
        Client code should use this static method instead of calling the constructor when loading a user.
        Fails if there is no user with the user id.

        Args:
            userid: User id of the user to load

        Returns: User object represented by the user id, None if no such user exists

        """

        user_doc = DBManager.get_instance().get_user_document_by_id(userid)
        if user_doc is None:
            return None

        user_obj = User()
        user_obj.__unpack_dict(user_doc)
        return user_obj

    def get_projects(self) -> list[str]:
        """Return a list of projects the user has access to.
        This list is a copy so that client code cannot modify the internal list

        Returns: A copy of the projects list

        """
        return self.__projects.copy()

    def _add_project(self, projectid: str) -> bool:
        """Add a project to the list the user has access to.
        Note: This method should not be called directly by the client since it does not actually grant the user access.
        Instead, the Project object should add the user to its authorized list and call this method on the user.

        Args:
            projectid: Project id that the user will gain access to

        Returns: True if successful, False otherwise

        """
        existed = projectid in self.__projects
        if not existed:
            self.__projects.append(projectid)

        return not existed

    def __pack_dict(self) -> dict:
        """Form a dict to insert into the database.
        """
        return {
            'username': self.__username,
            'userid': self.__userid,
            'password': self.__password,
            'projects': self.__projects,
        }

    def __unpack_dict(self, user_dict: dict) -> None:
        """Retrieve information from a dict stored in the database.
        """
        self.__username = user_dict['username']
        self.__userid = user_dict['userid']
        self.__password = user_dict['password']
        self.__projects = user_dict['projects']


# Example client code
if __name__ == '__main__':
    my_user = User.new_user(username='John Doe', userid='jd123', password='password123')
    print(f'Created new User: {my_user}')

    print(f'No projects: {my_user.get_projects()}')
    print(f'Adding a project: {my_user._add_project("pj123")}')
    print(f'One project: {my_user.get_projects()}')
    print(f'Adding same project: {my_user._add_project("pj123")}')
    print(f'One project: {my_user.get_projects()}')

    try:
        print('User.load_user is not implemented')
        my_user_again = User.load_user('jd123')
    except NotImplementedError as e:
        pass
