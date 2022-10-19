# Structure of MongoDB Database

1. We obtain a client connection to a MongoDB server.
2. We obtain a database (e.g. `Cluster0`) from the client.
3. We obtain three collections from the database. They are:
   - `Users`
   - `Projects`
   - `HWSet`
4. We can manipulate documents in each of the collections. Documents should have consistent form, so we detail a schema.

# Schema of MongoDB Documents

> The following schemas are just an example and may be subject to change.

Non-standard types used in the schemas for semantic purposes. They are listed here:

| Non-standard type | Underlying type | Purpose |
| ----------------- | --------------- | ------- |
| `userid_t` | `str` | Unique identity of a user. |
| `projectid_t` | `str` | Unique identity of a project. |
| `hwsetname_t` | `str` | Unique name of a hardware set. |

## Documents in `Users` Collection

```json
{
    "name": str,
    "userid": userid_t,
    "password": str,
    "projects": [projectid_t],
}
```

## Documents in `Projects` Collection

```json
{
    "projectid": projectid_t,
    "name": str,
    "description": str,
    "admin": userid_t,
    "users": [userid_t],
    "hwsets": [{
        "name": hwsetname_t,
        "checkedOut": int,
    }],
}
```

## Documents in `HWSet` Collection

```json
{
    "name": hwsetname_t,
    "capacity": int,
    "availability": int,
    "projects": [{
        "projectid": projectid_t,
        "checkedOut": int,
    }],
}
```
