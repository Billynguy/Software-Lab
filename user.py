from typing import Optional


class User:
    """Back-end representation of a user.
    """

    def __init__(self):
        """Client code should not directly call the constructor.
        Rather, client code should prefer the static `new_user` and `load_user` methods.
        """
        self._username: str = ''
        self._userid: str = ''
        self._password: str = ''
        self._projects: list[str] = []
        """This is a set of project ids."""

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
        # Check that another user with the same userid does not exist
        # if userid in user_collection:
        #     return None

        user = User()
        user._username = username
        user._userid = userid
        user._password = password
        return user

    @staticmethod
    def load_user(userid: str) -> Optional['User']:
        """Load a User object from its user id.
        Client code should use this static method instead of calling the constructor when loading a user.
        Fails if there is no user with the user id.

        Args:
            userid: User id of the user to load

        Returns: User object represented by the user id, None if no such user exists

        """
        # if userid in user_collection:
        #     return user_collection.get_user(userid)

        # return None
        raise NotImplementedError()

    def get_projects(self) -> list[str]:
        """Return a set of projects the user has access to.
        This set is a copy so that client code cannot modify the internal set

        Returns: A copy of the projects set

        """
        return self._projects.copy()

    def create_project(self, name: str, description: str) -> None:
        """Have the user create a new project.
        The user will become the project's manager.

        Args:
            name: Project name of the new project
            description: Project description of the new project

        """
        # This method might not be needed if the Project is created in the Project class
        # May return a Project object

        # Call a static create project method in Project class
        # self._projects.append(project.get_id())
        raise NotImplementedError()

    def authorize_user(self, projectid: str, userid: str) -> bool:
        """Authorize another user to access a project.
        Both projectid and userid must refer to a valid project and user respectively.
        The current user invoking authorize_user must have permission to do so.

        Args:
            projectid: Project id that the calling user must have admin access for
            userid: User id of a user that the calling user is authorizing

        Returns: True if successful, False otherwise

        """
        # This method might not be needed if the Project class implements an authorize_user class
        # May use exceptions instead if it is expected that client code validates parameters

        # Call an authorize user method in the Project object
        raise NotImplementedError

    def add_project(self, projectid: str) -> bool:
        """Add a project to the list the user has access to.
        Note: This method should not be called directly by the client since it does not actually grant the user access.
        Instead, the Project object should add the user to its authorized list and call this method on the user.

        Args:
            projectid: Project id that the user will gain access to

        Returns: True if successful, False otherwise

        """
        existed = projectid in self._projects
        if not existed:
            self._projects.append(projectid)

        return not existed


# Example client code
if __name__ == '__main__':
    my_user = User.new_user(username='John Doe', userid='jd123', password='password123')
    print(f'Created new User: {my_user}')

    print(f'No projects: {my_user.get_projects()}')
    print(f'Adding a project: {my_user.add_project("pj123")}')
    print(f'One project: {my_user.get_projects()}')
    print(f'Adding same project: {my_user.add_project("pj123")}')
    print(f'One project: {my_user.get_projects()}')

    try:
        print('User.load_user is not implemented')
        my_user_again = User.load_user('jd123')
    except NotImplementedError as e:
        pass

    try:
        print('User.create_project is not implemented')
        my_user.create_project('My project', "John Doe's project")
    except NotImplementedError as e:
        pass

    try:
        print('User.authorize_user is not implemented')
        my_user.authorize_user('pj123', 'ab456')
    except NotImplementedError as e:
        pass
