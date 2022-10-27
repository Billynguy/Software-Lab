from project import Project
from db_manager import DBManager, DBManagerMock
from test_db_manager import set_db_state, user_documents_some, project_documents_some, hwset_documents_some
from user import User
import warnings


def test_load_project():
    """Return project if found. Return None if not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('jd123') is not None
        assert Project.load_project('jp124') is not None
        assert Project.load_project('ECE 461L') is not None
        assert Project.load_project('DoesNotExist') is None


def test_new_project():
    """Return project if creation successful. Return None if projectid exists.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('pid378') is None
        assert Project.new_project('pid378', 'Project of Interesting Designs', 'We like Interesting Designs!', 'jd123') is not None
        assert Project.load_project('pid378') is not None
        assert Project.new_project('jp124', "Jane's second project", 'This project will fail...', 'jd124') is None
        assert Project.load_project('jp124') is not None


def test_get_projectid():
    """Return project's projectid.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('jd123').get_projectid() == 'jd123'
        assert Project.new_project('abc123', 'def456', 'efg789', 'jd123').get_projectid() == 'abc123'


def test_get_name():
    """Return project's name.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('jd123').get_name() == "John Doe's Project"
        assert Project.new_project('abc123', 'def456', 'efg789', 'jd123').get_name() == 'def456'


def test_get_description():
    """Return project's description.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('jd123').get_description() == "This is John Doe's first project."
        assert Project.new_project('abc123', 'def456', 'efg789', 'jd123').get_description() == 'efg789'


def test_get_admin():
    """Return project's admin.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert Project.load_project('jd123').get_admin() == 'jd123'
        assert Project.new_project('abc123', 'def456', 'efg789', 'jd123').get_admin() == 'jd123'


def test_has_user():
    """Return True if project has user. Return False if not.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        jp_project = Project.load_project('jp124')
        assert jp_project.has_user('jd124')
        assert jp_project.has_user('jd123')
        assert not jp_project.has_user('ece461')
        new_project = Project.new_project('new22', 'New Project', 'New project.', 'ece461')
        assert new_project.has_user('ece461')
        assert not new_project.has_user('jd123')


def test_get_users():
    """Return a list of users.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        users = Project.load_project('jp124').get_users()
        assert 'jd124' in users
        assert 'jd123' in users
        assert 'ece461' not in users
        assert 'ece461' in Project.new_project('new22', 'New Project', 'New project.', 'ece461').get_users()


def test_add_user():
    """If successful: Modify project's list. Modify user's list. Return True.
    Return None if user is already in the list.
    Return False if user does not exist or some other error.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        project = Project.load_project('ECE 461L')

        user = User.load_user('jd124')
        assert not project.has_user('jd124')
        assert 'ECE 461L' not in user.get_projects()

        assert project.add_user('jd124') is True
        user = User.load_user('jd124')
        assert project.has_user('jd124')
        assert 'ECE 461L' in user.get_projects()

        assert project.add_user('jd124') is None
        assert project.add_user('mmmmmmmmmmmmmmmmmmm') is False


def test_remove_user():
    """If successful: Modify project's list. Modify user's list. Return True.
    Return None if user is not in the list.
    Return False if user does not exist or some other error.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        project = Project.load_project('ECE 461L')

        user = User.load_user('jd123')
        assert project.has_user('jd123')
        assert 'ECE 461L' in user.get_projects()

        assert project.remove_user('jd123') is True
        user = User.load_user('jd123')
        assert not project.has_user('jd123')
        assert 'ECE 461L' not in user.get_projects()

        assert project.remove_user('jd123') is None
        assert project.remove_user('mmmmmmmmmmmmmmmmmmm') is False


def test_get_hwsets():
    """Return copy of hwsets dict.
    """
    warnings.warn('Project.get_hwsets() returns a dict instead of a list.')
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwsets = Project.load_project('jd123').get_hwsets()

        assert hwsets.get('Hardware Set 1', None) is not None
        assert hwsets.get('Hardware Set 2', None) is not None
        assert hwsets.get('Hardware Set 3', None) is None

        hwsets = Project.load_project('jp124').get_hwsets()
        assert hwsets.get('Hardware Set 1', None) is None
        assert hwsets.get('Hardware Set 3', None) is None

        hwsets = Project.load_project('ECE 461L').get_hwsets()
        assert hwsets.get('Hardware Set 1', None) is not None
        assert hwsets.get('Hardware Set 2', None) is not None
        assert hwsets.get('Hardware Set 3', None) is None


def check_has_hwset_list(projectid: str, hwsets: list[str]) -> bool:
    project = Project.load_project(projectid)
    assert project is not None
    project_hwsets = project.get_hwsets()
    for hwset_name in hwsets:
        if project_hwsets.get(hwset_name, None) is None:
            return False

    return True


def test_add_hwsets():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        project = Project.load_project('jp124')
        assert len(project.get_hwsets()) == 0

        assert project.add_hwsets('Hardware Set 2', 44) is True
        assert check_has_hwset_list('jp124', ['Hardware Set 2'])
        assert not check_has_hwset_list('jp124', ['Hardware Set 1'])
        project = Project.load_project('jp124')
        assert len(project.get_hwsets()) == 1

        assert project.add_hwsets('Hardware Set 2', 44) is True
        assert check_has_hwset_list('jp124', ['Hardware Set 2'])
        assert not check_has_hwset_list('jp124', ['Hardware Set 1'])
        project = Project.load_project('jp124')
        assert len(project.get_hwsets()) == 1

        assert project.add_hwsets('Hardware Set 1', 43) is True
        assert check_has_hwset_list('jp124', ['Hardware Set 1', 'Hardware Set 2'])


def test_remove_hwsets():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        project = Project.load_project('jd123')
        assert check_has_hwset_list('jd123', ['Hardware Set 1', 'Hardware Set 2'])

        assert project.remove_hwsets('Hardware Set 1', 80) is True
        assert check_has_hwset_list('jd123', ['Hardware Set 1', 'Hardware Set 2'])
        assert project.remove_hwsets('Hardware Set 1', 80) is False
        assert check_has_hwset_list('jd123', ['Hardware Set 1', 'Hardware Set 2'])
        assert project.remove_hwsets('Hardware Set 1', 20) is True
        assert check_has_hwset_list('jd123', ['Hardware Set 2'])
        assert not check_has_hwset_list('jd123', ['Hardware Set 1'])

        project = Project.load_project('jd123')
        assert len(project.get_hwsets()) == 1

        assert project.remove_hwsets('Hardware Set 1', 44) is None
        assert check_has_hwset_list('jd123', ['Hardware Set 2'])
        assert not check_has_hwset_list('jd123', ['Hardware Set 1'])


def test_example_client_code():
    """Cut, pasted, and modified from project.py.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        User.new_user(username='Johnny B', userid='jb123', password='password123')
        User.new_user(username='bn123', userid='bn123', password='bn123')
        Project.new_project(projectid='proj123', name='proj123', description='proj123', userid='jb123')

        my_project = Project.new_project(projectid='proj456', name='Project 2', description='This is my second test project', userid='jb123')
        assert my_project is not None

        my_project = Project.load_project('proj123')
        assert my_project is not None

        assert len(my_project.get_users()) == 1
        assert my_project.has_user('jb123')
        assert not my_project.has_user('bn123')

        assert my_project.add_user('bn123') is True
        assert len(my_project.get_users()) == 2
        assert my_project.has_user('jb123')
        assert my_project.has_user('bn123')

        assert my_project.add_user('bn123') is None
        assert len(my_project.get_users()) == 2
        assert my_project.has_user('jb123')
        assert my_project.has_user('bn123')

        assert my_project.remove_user('bn123') is True
        assert len(my_project.get_users()) == 1
        assert my_project.has_user('jb123')
        assert not my_project.has_user('bn123')

        assert my_project.remove_user('bn123') is None
        assert len(my_project.get_users()) == 1
        assert my_project.has_user('jb123')
        assert not my_project.has_user('bn123')

        assert len(my_project.get_hwsets()) == 0
        assert my_project.add_hwsets('Hardware Set 1', 10) is True
        assert len(my_project.get_hwsets()) == 1
        assert check_has_hwset_list('proj123', ['Hardware Set 1'])

        assert my_project.add_hwsets('Hardware Set 1', 5) is True
        assert len(my_project.get_hwsets()) == 1
        assert check_has_hwset_list('proj123', ['Hardware Set 1'])

        assert my_project.add_hwsets('Hardware Set 2', 10) is True
        assert len(my_project.get_hwsets()) == 2
        assert check_has_hwset_list('proj123', ['Hardware Set 1', 'Hardware Set 2'])

        assert my_project.remove_hwsets('Hardware Set 2', 5) is True
        assert len(my_project.get_hwsets()) == 2
        assert check_has_hwset_list('proj123', ['Hardware Set 1', 'Hardware Set 2'])

        assert my_project.remove_hwsets('Hardware Set 2', 5) is True
        assert len(my_project.get_hwsets()) == 1
        assert check_has_hwset_list('proj123', ['Hardware Set 1'])
        assert not check_has_hwset_list('proj123', ['Hardware Set 2'])

        assert my_project.remove_hwsets('Hardware Set 2', 5) is None
        assert len(my_project.get_hwsets()) == 1
        assert check_has_hwset_list('proj123', ['Hardware Set 1'])
        assert not check_has_hwset_list('proj123', ['Hardware Set 2'])

        assert my_project.remove_hwsets('Hardware Set 1', 15) is True
        assert len(my_project.get_hwsets()) == 0
        assert not check_has_hwset_list('proj123', ['Hardware Set 1'])
        assert not check_has_hwset_list('proj123', ['Hardware Set 2'])

        assert Project.load_project('proj123') is not None
