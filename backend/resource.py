from flask import Blueprint, make_response

resource_bp = Blueprint('resource', __name__)
"""Blueprint for api requests related to resource information.
"""


@resource_bp.get('/resource/<string:hwset>/resource-info')
def __resource_get_resource_info_for(hwset: str):
    """Get the hardware set's name, capacity, and availability.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing hardware set's name, capacity, and availability or 404 error
    """

    # resource = get_hwset_collection().get_hwset(hwset)
    # if resource is None:
    return make_response({
        'status': {
            'success': False,
            'reason': 'Unable to get resource information.',
        }
    }, 404)

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'name': resource.get_name(),
    #         'capacity': resource.get_capacity(),
    #         'availability': resource.get_availability(),
    #     }
    # }, 200)


@resource_bp.get('/resource/resource-info')
def __resource_get_resource_info():
    """Get all hardware sets' name, capacity, and availability.

    We make all types of errors look identical to make it harder to reverse engineer.
    :return: json response with data containing resource info or 404 error if not
    """

    # resources = []
    # for resource in get_hwset_collection():
    #     resources.append({
    #         'name': resource.get_name(),
    #         'capacity': resource.get_capacity(),
    #         'availability': resource.get_availability(),
    #     })

    # return make_response({
    #     'status': {
    #         'success': True,
    #     },
    #     'data': {
    #         'resources': resources
    #     }
    # }, 200)

    return make_response({
        'status': {
            'success': False,
            'reason': 'Unable to get resource information.',
        }
    }, 404)
