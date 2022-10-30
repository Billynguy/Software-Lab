from flask import Blueprint, make_response
from hardware_set import HWSet
from db_manager import DBManager

resource_bp = Blueprint('resource', __name__)
"""Blueprint for api requests related to resource information.
"""

"""Resource information.
"""


@resource_bp.get('/resource/<string:hwset_name>/resource-info')
def resource_get_resource_info_for(hwset_name: str):
    """Get the hardware set's name, capacity, and availability.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing hardware set's name, capacity, and availability or 404 error
    """

    hwset = HWSet.load_hwset(hwset_name)
    if hwset is None:
        return make_response({
            'status': {
                'success': False,
                'reason': 'Unable to get resource information.',
            }
        }, 404)

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'name': hwset_name,
            'capacity': hwset.get_capacity(),
            'availability': hwset.get_availability(),
        }
    }, 200)


@resource_bp.get('/resource/resource-info')
def resource_get_resource_info():
    """Get all hardware sets' name, capacity, and availability.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing resource info or 404 error if not
    """

    resources = []
    for hwset_doc in DBManager.get_instance().get_hwsets_collection().find():
        resources.append({
            'name': hwset_doc['name'],
            'capacity': hwset_doc['capacity'],
            'availability': hwset_doc['availability'],
        })

    return make_response({
        'status': {
            'success': True,
        },
        'data': {
            'resources': resources
        }
    }, 200)
