from user import User
from db_manager import DBManager, DBManagerMock
from test_db_manager import set_db_state, user_documents_some, project_documents_some, hwset_documents_some


def test_load_user():
    """Return user if found. Return None if not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert User.load_user('jd123') is not None
        assert User.load_user('jd124') is not None
        assert User.load_user('ece461') is not None
        assert User.load_user('ex404') is None


def test_new_user():
    """Return user if creation successful. Return None if userid exists.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert User.load_user('ao637') is None
        assert User.new_user('Apollo Orchestration', 'ao637', '5&mL!c#') is not None
        assert User.load_user('ao637') is not None
        assert User.new_user('Jefferson Davis', 'jd124', '6(2Mv<}') is None
        assert User.load_user('jd124') is not None


def test_get_username():
    """Return user's username.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert User.load_user('jd123').get_username() == 'John Doe'


def test_get_userid():
    """Return user's userid.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert User.new_user('Apples and Oranges Ltd.', 'ao637', 'c(25K1fL42N25)').get_userid() == 'ao637'
        assert User.load_user('jd124').get_userid() == 'jd124'


def test_matches_password():
    """Return user's userid.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert User.load_user('jd123').matches_password('password123')
        assert not User.load_user('jd123').matches_password('password12')
        assert not User.load_user('jd123').matches_password('password1234')
        assert not User.load_user('jd124').matches_password('password123')
        assert User.load_user('jd124').matches_password('8017d697e018d804f2436a3aaa8936ed57b75074')


def check_has_project_list(userid: str, projects: list[str]) -> bool:
    user = User.load_user(userid)
    assert user is not None
    user_projects = user.get_projects()
    for projectid in projects:
        if projectid not in user_projects:
            return False

    return True


def test_get_projects():
    """Return a list of projectid's that the user is a part of.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        expected_projects = ['jd123', 'ECE 461L']
        user_projects = User.load_user('jd123').get_projects()
        assert len(user_projects) == len(expected_projects)
        assert check_has_project_list('jd123', expected_projects)

        expected_projects = []
        user_projects = User.new_user('Aaron Aardvark', 'aa1111', 'aA11!aA!a11a!').get_projects()
        assert len(user_projects) == len(expected_projects)
        assert check_has_project_list('aa1111', expected_projects)


def test_add_project():
    """Add a projectid if not already in list. Return if successful.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        user = User.load_user('jd123')
        user_projects = user.get_projects()
        assert len(user_projects) == 2
        assert check_has_project_list('jd123', ['jd123', 'ECE 461L'])

        assert user.add_project('jp124') is True
        assert check_has_project_list('jd123', ['jd123', 'ECE 461L', 'jp124'])

        assert user.add_project('jp124') is False
        assert check_has_project_list('jd123', ['jd123', 'ECE 461L', 'jp124'])


def test_remove_project():
    """Remove a projectid if in list. Return if successful.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        user = User.load_user('jd123')
        user_projects = user.get_projects()
        assert len(user_projects) == 2
        assert check_has_project_list('jd123', ['jd123', 'ECE 461L'])

        assert user.remove_project('ECE 461L') is True
        assert check_has_project_list('jd123', ['jd123'])
        assert not check_has_project_list('jd123', ['jd123', 'ECE 461L'])

        assert user.remove_project('jp124') is False
        assert check_has_project_list('jd123', ['jd123'])
        assert not check_has_project_list('jd123', ['jp124'])


def test_example_client_code():
    """Cut, pasted, and modified from user.py.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())

        my_user = User.load_user('jd123')
        assert my_user is not None

        my_user = User.new_user(username='Johnny B', userid='jb123', password='password123')
        assert my_user is not None

        assert len(my_user.get_projects()) == 0

        assert my_user.add_project('pj123') is True
        assert len(my_user.get_projects()) == 1
        assert check_has_project_list('jb123', ['pj123'])

        assert my_user.add_project('pj123') is False
        assert len(my_user.get_projects()) == 1
        assert check_has_project_list('jb123', ['pj123'])

        assert my_user.remove_project('pj123') is True
        assert len(my_user.get_projects()) == 0
        assert not check_has_project_list('jb123', ['pj123'])

        assert my_user.remove_project('pj123') is False
        assert len(my_user.get_projects()) == 0
        assert not check_has_project_list('jb123', ['pj123'])

        assert User.load_user('jd123') is not None
