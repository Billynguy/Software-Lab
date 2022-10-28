from hardware_set import HWSet
from db_manager import DBManager, DBManagerMock
from test_db_manager import set_db_state, user_documents_some, project_documents_some, hwset_documents_some
from project import Project
import warnings


def test_load_hwset():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert HWSet.load_hwset('Hardware Set 1') is not None
        assert HWSet.load_hwset('Hardware Set 2') is not None
        assert HWSet.load_hwset('Hardware Set 3') is None


def test_new_hwset():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        warnings.warn('HWSet.new_hwset() does not fail when trying to create a new hardware set resource with the same name.')
        assert HWSet.new_hwset('Hardware Set 1', 1000) is None
        assert HWSet.new_hwset('Hardware Set 2', 1000) is None
        assert HWSet.new_hwset('Hardware Set 3', 1000) is not None
        assert HWSet.new_hwset('3080', 1000) is not None


def test_get_capacity():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert HWSet.load_hwset('Hardware Set 1').get_capacity() == 500
        assert HWSet.load_hwset('Hardware Set 2').get_capacity() == 377
        assert HWSet.new_hwset('Hardware Set 3', 23451).get_capacity() == 23451


def test_get_availability():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        assert HWSet.load_hwset('Hardware Set 1').get_availability() == 300
        assert HWSet.load_hwset('Hardware Set 2').get_availability() == 277
        assert HWSet.new_hwset('Hardware Set 3', 23451).get_availability() == 23451


def test_change_capacity():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        warnings.warn('HWSet.change_capacity() sets availability to amount even if some units are checked out.')
        warnings.warn('HWSet.change_capacity() does not handle bad requests.')

        hwset1 = HWSet.load_hwset('Hardware Set 1')
        assert hwset1.get_capacity() == 500
        assert hwset1.get_availability() == 300
        assert hwset1.change_capacity(600) is True
        assert hwset1.get_capacity() == 600
        assert hwset1.get_availability() == 400

        hwset2 = HWSet.load_hwset('Hardware Set 2')
        assert hwset2.get_capacity() == 377
        assert hwset2.get_availability() == 277
        assert hwset2.change_capacity(100) is True
        assert hwset2.get_capacity() == 100
        assert hwset2.get_availability() == 0
        assert hwset2.change_capacity(99) is False
        assert hwset2.get_capacity() == 100
        assert hwset2.get_availability() == 0


def test_get_projects():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwset1 = HWSet.load_hwset('Hardware Set 1')
        assert 'jd123' in hwset1.get_projects()
        assert 'ECE 461L' in hwset1.get_projects()
        assert 'jp124' not in hwset1.get_projects()

        hwset3 = HWSet.new_hwset('Hardware Set 3', 3)
        assert len(hwset3.get_projects()) == 0


def test_has_project():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwset2 = HWSet.load_hwset('Hardware Set 2')
        assert hwset2.has_project('jd123')
        assert hwset2.has_project('ECE 461L')
        assert not hwset2.has_project('jp124')


def check_has_projectid_list(hwset_name: str, projectids: list[str]) -> bool:
    hwset = HWSet.load_hwset(hwset_name)
    assert hwset is not None
    for projectid in projectids:
        if not hwset.has_project(projectid):
            return False

    return True


def test_get_checked_out():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwset1 = HWSet.load_hwset('Hardware Set 1')
        assert hwset1.get_checked_out('jd123') == 100
        assert hwset1.get_checked_out('jp124') == 0
        assert hwset1.get_checked_out('ECE 461L') == 100

        hwset3 = HWSet.new_hwset('Hardware Set 3', 333)
        assert hwset3.get_checked_out('jd123') == 0
        assert hwset3.get_checked_out('jp124') == 0
        assert hwset3.get_checked_out('ECE 461L') == 0


def test_check_out():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwset2 = HWSet.load_hwset('Hardware Set 2')
        assert hwset2.get_availability() == 277
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'ECE 461L'])
        assert not check_has_projectid_list('Hardware Set 2', ['jp124'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 20
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 0
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_out('jd123', 200) is True
        assert hwset2.get_availability() == 77
        assert not check_has_projectid_list('Hardware Set 2', ['jp124'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 220
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 0
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_out('dne4145', 76) is False
        assert hwset2.get_availability() == 77
        assert not check_has_projectid_list('Hardware Set 2', ['jp124'])
        assert not check_has_projectid_list('Hardware Set 2', ['dne4145'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 220
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 0
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_out('jp124', 76) is True
        assert hwset2.get_availability() == 1
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'jp124', 'ECE 461L'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 220
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 76
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_out('jd123', 2) is False
        assert hwset2.get_availability() == 1
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'jp124', 'ECE 461L'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 220
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 76
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80


def test_check_in():
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        hwset2 = HWSet.load_hwset('Hardware Set 2')
        assert hwset2.get_availability() == 277
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'ECE 461L'])
        assert not check_has_projectid_list('Hardware Set 2', ['jp124'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 20
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 0
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_in('jd123', 2) is True
        assert hwset2.get_availability() == 279
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'ECE 461L'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 18
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_in('dne4145', 76) is False
        assert hwset2.get_availability() == 279
        assert not check_has_projectid_list('Hardware Set 2', ['dne4145'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 18
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_in('jp124', 76) is None
        assert hwset2.get_availability() == 279
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'ECE 461L'])
        assert not check_has_projectid_list('Hardware Set 2', ['jp124'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 18
        assert Project.load_project('jp124').get_hwsets().get('Hardware Set 2', 0) == 0
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80

        assert hwset2.check_in('jd123', 222) is False
        assert hwset2.get_availability() == 279
        assert check_has_projectid_list('Hardware Set 2', ['jd123', 'ECE 461L'])
        assert Project.load_project('jd123').get_hwsets().get('Hardware Set 2', 0) == 18
        assert Project.load_project('ECE 461L').get_hwsets().get('Hardware Set 2', 0) == 80



def test_example_client_code():
    """Cut, pasted, and modified from hardware_set.py.
    """
    with DBManager.get_instance(underlying_class=DBManagerMock) as db_manager:
        set_db_state(db_manager, user_documents_some(), project_documents_some(), hwset_documents_some())
        my_hwset = HWSet.new_hwset(name='HW123', capacity=1000)
        assert my_hwset is not None
        my_hwset = HWSet.load_hwset(name='HW123')
        assert my_hwset is not None

        assert my_hwset.get_capacity() == 1000
        assert my_hwset.get_availability() == 1000
        assert my_hwset.change_capacity(100) is True
        assert my_hwset.get_capacity() == 100
        assert my_hwset.get_availability() == 100
        assert my_hwset.change_capacity(1000) is True
        assert my_hwset.get_capacity() == 1000
        assert my_hwset.get_availability() == 1000

        Project.new_project('proj123', 'proj123', 'proj123', 'ece461')
        Project.new_project('proj456', 'proj456', 'proj456', 'ece461')

        assert my_hwset.check_out('proj123', 500) is True
        assert my_hwset.get_availability() == 500
        assert my_hwset.has_project('proj123')
        assert len(my_hwset.get_projects()) == 1
        assert Project.load_project('proj123').get_hwsets()['HW123'] == 500

        assert my_hwset.check_out('proj456', 200) is True
        assert my_hwset.get_availability() == 300
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 200

        assert my_hwset.check_out('proj456', 200) is True
        assert my_hwset.get_availability() == 100
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 400

        assert my_hwset.check_out('proj456', 200) is False
        assert my_hwset.get_availability() == 100
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 400

        assert my_hwset.check_out('projNA', 200) is False
        assert my_hwset.get_availability() == 100
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert not my_hwset.has_project('projNA')
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 400

        assert my_hwset.check_out('proj456', 100) is True
        assert my_hwset.get_availability() == 0
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 500

        assert my_hwset.check_in('projNA', 250) is False
        assert my_hwset.get_availability() == 0
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert not my_hwset.has_project('projNA')
        assert len(my_hwset.get_projects()) == 2

        assert my_hwset.check_in('proj456', 250) is True
        assert my_hwset.get_availability() == 250
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 250

        assert my_hwset.check_in('proj456', 500) is False
        assert my_hwset.get_availability() == 250
        assert check_has_projectid_list('HW123', ['proj123', 'proj456'])
        assert len(my_hwset.get_projects()) == 2
        assert Project.load_project('proj456').get_hwsets()['HW123'] == 250

        assert my_hwset.check_in('proj456', 250) is True
        assert my_hwset.get_availability() == 500
        assert check_has_projectid_list('HW123', ['proj123'])
        assert not check_has_projectid_list('HW123', ['proj456'])
        assert len(my_hwset.get_projects()) == 1
        assert Project.load_project('proj456').get_hwsets().get('HW123', 0) == 0

        assert my_hwset.check_in('proj123', 500) is True
        assert my_hwset.get_availability() == 1000
        assert not check_has_projectid_list('HW123', ['proj123'])
        assert not check_has_projectid_list('HW123', ['proj456'])
        assert len(my_hwset.get_projects()) == 0
        assert Project.load_project('proj123').get_hwsets().get('HW123', 0) == 0
