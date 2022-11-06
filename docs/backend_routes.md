# Back-end Routes

> Note: This document may be out of date since these routes may be subject to change.\
  To get the most up-to-date routes, type `flask routes` and/or open the `*_routes.py` files.

Unless otherwise specified, the json objects returned by these routes are of the form:

```json
{
    "status": {
        "success": true, // or false
        "reason": "some string", // Must exist if success is false, cannot exist if success is true
    },
    "data": { // Cannot exist if success is false, may or may not exist if success is true
        // Some data here
    }
}
```

## User Routes

| Rule | Method | Inputs | Description |
| ---- | ------ | ------ | ----------- |
| `/api/sign-in/` | `POST` | FormData containing `userid` and `password` | On success, data contains `userid` and sets `session`. |
| `/api/sign-up/` | `POST` | FormData containing `userid` and `password` | On success, data contains `userid` and sets `session`. |
| `/api/sign-out/` | `GET` | Route should be directly accessed, not `fetch`'d | On success, returns nothing and clears `session`. |
| `/api/user/<string:userid>/user-info/` | `GET` | `userid` in route should match `session` | On success, data contains `username` and `userid`. |
| `/api/user/<string:userid>/project-list/` | `GET` | `userid` in route should match `session` | On success, data contains `projects`, an array of project ids. |

## Project Routes

| Rule | Method | Inputs | Description |
| ---- | ------ | ------ | ----------- |
| `/api/open-project/` | `GET` | FormData containing `projectid`; `session` user should be authorized | On success, returns no data. |
| `/api/create-project/` | `POST` | FormData containing `projectid`, `name`, and `description`; `session` should be set | On success, data contains `projectid`. |
| `/api/project/<string:projectid>/authorize-user` | `POST` | `projectid` in route should exist; `session` user should be project's admin; FormData containing `userid` | On success, returns no data. |
| `/api/project/<string:projectid>/revoke-user` | `POST` | `projectid` in route should exist; `session` user should be project's admin; FormData containing `userid` | On success, returns no data. |
| `/api/project/<string:projectid>/project-info` | `GET` | `projectid` in route should exist; `session` user should be authorized | On success, data contains `name`, `projectid`, and `description`. |
| `/api/project/<string:projectid>/user-list` | `GET` | `projectid` in route should exist; `session` user should be authorized | On success, data contains `users`, an array of user ids. |
| `/api/project/<string:projectid>/is-session-admin` | `GET` | `projectid` in route should exist; `session` user should be project's admin | On success, data contains `isAdmin` always true. |

### Project-Resource Routes

| Rule | Method | Inputs | Description |
| ---- | ------ | ------ | ----------- |
| `/api/project/<string:projectid>/update-resources` | `POST` | `projectid` in route should exist; `session` user should be authorized; FormData containing `<hwset_name>-checkout` | On success, return no data. |
| `/api/project/<string:projectid>/add-resource` | `POST` | `projectid` in route should exist; `session` user should be authorized; FormData containing `name` | On success, returns no data. |
| `/api/project/<string:projectid>/remove-resource` | `POST` | `projectid` in route should exist; `session` user should be authorized; FormData containing `name` | On success, returns no data. |
| `/api/project/<string:projectid>/resources` | `GET` | `projectid` in route should exist; `session` user should be authorized  | On success, data contains `resources`, an array containing objects. These objects contain `name`, <br>if resource exists: `availability`, `checkedOut`, and `unused` (if `checkedOut` is 0), <br>if resource does not exist: `noSuchObject` always true. |

## Resource Routes

| Rule | Method | Inputs | Description |
| ---- | ------ | ------ | ----------- |
| `/api/resource/<string:hwset_name>/resource-info` | `GET` | `hwset_name` in route should exist | On success, data contains `name`, `capacity`, and `availability`. |
| `/api/resource/resource-info` | `GET` | None | On success, data contains `resources`, an array containing objects. These objects contain `name`, `capacity`, and `availability`. |

## Test Routes

| Rule | Method | Inputs | Description |
| ---- | ------ | ------ | ----------- |
| `/` | `GET` | None | On success, returns the string "Hello, World!". |
| `/api/get-test` | `GET` | None | On success, returns `{"string": "This is a string from the api.}`. |
| `/api/post-test` | `GET` | None | On success, returns an HTML form. |
| `/api/post-test` | `POST` | Optional FormData containing `string` | On success, returns either `{"response": "No string was sent."}` or `{"response": "This is your string: \"<string>\""}` where `<string>` is from FormData. |
