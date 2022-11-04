from db_manager import DBManager, DBManagerMock
import warnings


def user_documents_some() -> list[dict]:
    user_docs = [
        {
            'userid': 'jd123',
            'username': 'John Doe',
            # Password is 'password123'
            'password': 'pbkdf2:sha256:260000$YzfiDWPGT4a539En$c2bac2c14f5f51ab1f57be178c6a406c749f3fc46c6bfa7aab06d843ae5cf55f',
            'projects': ['jd123', 'ECE 461L', ],
        },
        {
            'userid': 'jd124',
            'username': 'Jane Doe',
            # Password is '8017d697e018d804f2436a3aaa8936ed57b75074'
            'password': 'pbkdf2:sha256:260000$t24LYP3cVG6ne2ii$5957fa81790f193807a38858bb425315e5b4354b96bef7836a032a4506fb2ddb',
            'projects': ['jd123', 'jp124', ],
        },
        {
            'userid': 'ece461',
            'username': 'Test User',
            # Password is '8017d697e018d804f2436a3aaa8936ed57b75074'
            'password': 'pbkdf2:sha256:260000$t24LYP3cVG6ne2ii$5957fa81790f193807a38858bb425315e5b4354b96bef7836a032a4506fb2ddb',
            'projects': ['ECE 461L', ],
        },
    ]

    return user_docs


def project_documents_some() -> list[dict]:
    project_docs = [
        {
            'projectid': 'jd123',
            'name': "John Doe's Project",
            'description': "This is John Doe's first project.",
            'admin': 'jd123',
            'users': ['jd123', ],
            'hwsets': {
                'Hardware Set 1': 100,
                'Hardware Set 2': 20,
            },
        },
        {
            'projectid': 'jp124',
            'name': "Jane Doe's Project",
            'description': 'Hello, World!',
            'admin': 'jd124',
            'users': ['jd124', 'jd123', ],
            'hwsets': {},
        },
        {
            'projectid': 'ECE 461L',
            'name': 'Test Project',
            'description': "This is a test project.",
            'admin': 'ece461',
            'users': ['ece461', 'jd123'],
            'hwsets': {
                'Hardware Set 1': 100,
                'Hardware Set 2': 80,
            },
        },
    ]

    return project_docs


def hwset_documents_some() -> list[dict]:
    hwset_docs = [
        {
            'name': 'Hardware Set 1',
            'capacity': 500,
            'availability': 300,
            'projects': {
                'jd123': 100,
                'ECE 461L': 100,
            },
        },
        {
            'name': 'Hardware Set 2',
            'capacity': 377,
            'availability': 277,
            'projects': {
                'jd123': 20,
                'ECE 461L': 80,
            },
        },
    ]

    return hwset_docs


def set_db_state(db_manager: DBManager, user_documents: list[dict], project_documents: list[dict], hwset_documents: list[dict]) -> None:
    for user_doc in user_documents:
        db_manager.insert_user_document(user_doc)
    for project_doc in project_documents:
        db_manager.insert_project_document(project_doc)
    for hwset_doc in hwset_documents:
        db_manager.insert_hwset_document(hwset_doc)


def test_get_instance():
    """The instance returned should be the same instance as the class instance.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        other_instance = DBManager.get_instance()
        assert other_instance is db_manager


def test_close():
    """A new instance cannot be created even after close.
    """
    db_manager = DBManager.get_instance(underlying_class=DBManagerMock)
    db_manager.close()
    other_instance = DBManager.get_instance()
    assert other_instance is db_manager


def test_get_user_document_by_id():
    """Return a user doc if found. Return None if not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert db_manager.get_user_document_by_id('jd123') is not None
        assert db_manager.get_user_document_by_id('ece461') is not None
        assert db_manager.get_user_document_by_id('alg245') is None


def check_has_userid_list(db_manager: DBManager, userid_list: list[str]) -> bool:
    for userid in userid_list:
        if db_manager.get_user_document_by_id(userid) is None:
            return False
    return True


def check_user_matches(db_manager: DBManager, user_document: dict) -> bool:
    assert user_document.get('userid', None) is not None
    user_doc = db_manager.get_user_document_by_id(user_document['userid'])
    assert user_doc is not None
    for key, value in user_document.items():
        if user_doc[key] != value:
            return False
    return True


def test_insert_user_document():
    """Return true if inserting new user. Return false if userid exists.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        assert check_has_userid_list(db_manager, [])
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert check_has_userid_list(db_manager, ['jd123', 'jd124', 'ece461'])
        assert check_user_matches(db_manager, {
            'userid': 'jd123',
            'username': 'John Doe',
            # Password is 'password123'
            'password': 'pbkdf2:sha256:260000$YzfiDWPGT4a539En$c2bac2c14f5f51ab1f57be178c6a406c749f3fc46c6bfa7aab06d843ae5cf55f',
            'projects': ['jd123', 'ECE 461L'],
        })
        new_user_doc = {
            'userid': 'az78705',
            'username': 'Alice Zoey',
            # Password is 'bRQ$v&+'
            'password': 'pbkdf2:sha256:260000$OSQJM8VSXhrRFIJQ$d82f3cb7e3a37f0126bfd0cea0f679a80054f90e13146a7c5e091c5608b758d9',
            'projects': [],
        }
        assert db_manager.insert_user_document(new_user_doc) is True
        assert check_has_userid_list(db_manager, ['jd123', 'jd124', 'ece461', 'az78705'])
        assert check_user_matches(db_manager, {
            'userid': 'az78705',
            'username': 'Alice Zoey',
            'projects': [],
        })

        conflict_user_doc = {
            'userid': 'jd123',
            'username': 'JD',
            # Password is 'j%36mVK*'
            'password': 'pbkdf2:sha256:260000$N2cGfHdMQFQxaHtC$d1925b63379171e89173dd4022ed491236890043369295157e0871f867364fbd',
            'projects': [],
        }
        assert db_manager.insert_user_document(conflict_user_doc) is False
        assert check_has_userid_list(db_manager, ['jd123', 'jd124', 'ece461', 'az78705'])
        assert not check_user_matches(db_manager, {
            'userid': 'jd123',
            'username': 'JD'
        })
        assert check_user_matches(db_manager, {
            'userid': 'jd123',
            'username': 'John Doe'
        })


def test_update_user_document():
    """Return true if user found and updated. Return false if user not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        existing_user_doc = {
            'userid': 'jd123',
            'username': 'JD',
            # Password is 'j%36mVK*'
            'password': 'pbkdf2:sha256:260000$N2cGfHdMQFQxaHtC$d1925b63379171e89173dd4022ed491236890043369295157e0871f867364fbd',
        }
        assert db_manager.update_user_document(existing_user_doc, 'username') is True
        assert check_user_matches(db_manager, {
            'userid': 'jd123',
            'username': 'JD',
            # Password is 'password123'
            'password': 'pbkdf2:sha256:260000$YzfiDWPGT4a539En$c2bac2c14f5f51ab1f57be178c6a406c749f3fc46c6bfa7aab06d843ae5cf55f',
        })
        assert db_manager.update_user_document(existing_user_doc, 'password') is True
        assert check_user_matches(db_manager, {
            'userid': 'jd123',
            'username': 'JD',
            # Password is 'j%36mVK*'
            'password': 'pbkdf2:sha256:260000$N2cGfHdMQFQxaHtC$d1925b63379171e89173dd4022ed491236890043369295157e0871f867364fbd',
        })

        new_user_doc = {
            'userid': 'az78705',
            'username': 'Alice Zoey',
            # Password is 'bRQ$v&+'
            'password': 'pbkdf2:sha256:260000$OSQJM8VSXhrRFIJQ$d82f3cb7e3a37f0126bfd0cea0f679a80054f90e13146a7c5e091c5608b758d9',
            'projects': [],
        }
        assert db_manager.update_user_document(new_user_doc, 'username') is False
        assert db_manager.update_user_document(new_user_doc, 'password') is False
        assert not check_has_userid_list(db_manager, ['az78705'])


def test_get_project_document_by_id():
    """Return a project doc if found. Return None if not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert db_manager.get_project_document_by_id('jd123') is not None
        assert db_manager.get_project_document_by_id('jp124') is not None
        assert db_manager.get_project_document_by_id('alg') is None


def check_has_projectid_list(db_manager: DBManager, projectid_list: list[str]) -> bool:
    for projectid in projectid_list:
        if db_manager.get_project_document_by_id(projectid) is None:
            return False
    return True


def check_project_matches(db_manager: DBManager, project_document: dict) -> bool:
    assert project_document.get('projectid', None) is not None
    project_doc = db_manager.get_project_document_by_id(project_document['projectid'])
    assert project_doc is not None
    for key, value in project_document.items():
        if project_doc[key] != value:
            return False
    return True


def test_insert_project_document():
    """Return true if inserting new project. Return false if projectid exists.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        assert check_has_projectid_list(db_manager, [])
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert check_has_projectid_list(db_manager, ['jd123', 'jp124', 'ECE 461L'])
        assert check_project_matches(db_manager, {
            'projectid': 'jd123',
            'name': "John Doe's Project",
            'description': "This is John Doe's first project.",
            'admin': 'jd123',
            'users': ['jd123'],
            'hwsets': {
                'Hardware Set 1': 100,
                'Hardware Set 2': 20,
            },
        })
        new_project_doc = {
            'projectid': 'pq96',
            'name': 'Funny Symbols',
            'description': 'We have some funny symbols here.',
            'admin': 'jd124',
            'users': ['jd124'],
            'hwsets': {},
        }
        assert db_manager.insert_project_document(new_project_doc) is True
        assert check_has_projectid_list(db_manager, ['jd123', 'jp124', 'ECE 461L', 'pq96'])
        assert check_project_matches(db_manager, {
            'projectid': 'pq96',
            'name': 'Funny Symbols',
            'admin': 'jd124',
            'users': ['jd124'],
            'hwsets': {},
        })

        conflict_project_doc = {
            'projectid': 'ECE 461L',
            'name': 'Test Project Prime',
            'description': 'This is a different test project.',
            'admin': 'ece461',
            'users': ['ece461', 'jd123'],
            'hwsets': {},
        }
        assert db_manager.insert_project_document(conflict_project_doc) is False
        assert check_has_projectid_list(db_manager, ['jd123', 'jp124', 'ECE 461L', 'pq96'])
        assert not check_project_matches(db_manager, {
            'projectid': 'ECE 461L',
            'name': 'Test Project Prime'
        })
        assert check_project_matches(db_manager, {
            'projectid': 'ECE 461L',
            'name': 'Test Project'
        })


def test_update_project_document():
    """Return true if project found and updated. Return false if project not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        existing_project_doc = {
            'projectid': 'ECE 461L',
            'name': 'Test Project Prime',
            'description': 'This is a different test project.',
        }
        assert db_manager.update_project_document(existing_project_doc, 'name') is True
        assert check_project_matches(db_manager, {
            'projectid': 'ECE 461L',
            'name': 'Test Project Prime',
            'description': 'This is a test project.',
        })
        assert db_manager.update_project_document(existing_project_doc, 'description') is True
        assert check_project_matches(db_manager, {
            'projectid': 'ECE 461L',
            'name': 'Test Project Prime',
            'description': 'This is a different test project.',
        })

        new_project_doc = {
            'projectid': 'pq96',
            'name': 'Funny Symbols',
            'description': 'We have some funny symbols here.',
            'admin': 'jd124',
            'users': ['jd124'],
            'hwsets': {},
        }
        assert db_manager.update_project_document(new_project_doc, 'name') is False
        assert db_manager.update_project_document(new_project_doc, 'description') is False
        assert not check_has_projectid_list(db_manager, ['pq96'])


def test_get_hwset_document_by_name():
    """Return a project doc if found. Return None if not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert db_manager.get_hwset_document_by_name('Hardware Set 1') is not None
        assert db_manager.get_hwset_document_by_name('Hardware Set 2') is not None
        assert db_manager.get_hwset_document_by_name('Hardware Set 3') is None


def check_has_hwsetname_list(db_manager: DBManager, hwsetname_list: list[str]) -> bool:
    for hwsetname in hwsetname_list:
        if db_manager.get_hwset_document_by_name(hwsetname) is None:
            return False
    return True


def check_hwset_matches(db_manager: DBManager, hwset_document: dict) -> bool:
    assert hwset_document.get('name', None) is not None
    hwset_doc = db_manager.get_hwset_document_by_name(hwset_document['name'])
    assert hwset_doc is not None
    for key, value in hwset_document.items():
        if hwset_doc[key] != value:
            return False
    return True


def test_insert_hwset_document():
    """Return true if inserting new hwset. Return false if hwset with name exists.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        assert check_has_hwsetname_list(db_manager, [])
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert check_has_hwsetname_list(db_manager, ['Hardware Set 1', 'Hardware Set 2'])
        assert check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 500,
            'availability': 300,
            'projects': {
                'jd123': 100,
                'ECE 461L': 100,
            },
        })

        new_hwset_doc = {
            'name': 'New Super HWSet',
            'capacity': 999,
            'availability': 999,
            'projects': {},
        }
        assert db_manager.insert_hwset_document(new_hwset_doc) is True
        assert check_has_hwsetname_list(db_manager, ['Hardware Set 1', 'Hardware Set 2', 'New Super HWSet'])
        assert check_hwset_matches(db_manager, {
            'name': 'New Super HWSet',
            'capacity': 999,
            'availability': 999,
            'projects': {},
        })

        conflict_hwset_doc = {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 600,
            'projects': {},
        }
        warnings.warn('Inserting a new hardware set with the same name should fail.')
        assert db_manager.insert_hwset_document(conflict_hwset_doc) is False
        assert check_has_hwsetname_list(db_manager, ['Hardware Set 1', 'Hardware Set 2', 'New Super HWSet'])
        assert not check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 600,
        })
        assert check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 500,
            'availability': 300,
        })


def test_update_hwset_document():
    """Return true if hwset found and updated. Return false if hwset not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        existing_hwset_doc = {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 400,
        }
        assert db_manager.update_hwset_document(existing_hwset_doc, 'capacity') is True
        assert check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 300,
        })
        assert db_manager.update_hwset_document(existing_hwset_doc, 'availability') is True
        assert check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 400,
        })

        new_hwset_doc = {
            'name': 'New Super HWSet',
            'capacity': 999,
            'availability': 999,
        }
        assert db_manager.update_hwset_document(new_hwset_doc, 'capacity') is False
        assert db_manager.update_hwset_document(new_hwset_doc, 'availability') is False
        assert not check_has_hwsetname_list(db_manager, ['New Super HWSet'])


def test_update_hwset_document_multiple():
    """Return true if hwset found and updated. Return false if hwset not found.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        existing_hwset_doc = {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 400,
        }
        assert db_manager.update_hwset_document_multiple(existing_hwset_doc, 'capacity', 'availability') is True
        assert check_hwset_matches(db_manager, {
            'name': 'Hardware Set 1',
            'capacity': 600,
            'availability': 400,
        })

        new_hwset_doc = {
            'name': 'New Super HWSet',
            'capacity': 999,
            'availability': 999,
        }
        assert db_manager.update_hwset_document_multiple(new_hwset_doc, 'capacity', 'availability') is False
        assert not check_has_hwsetname_list(db_manager, ['New Super HWSet'])
