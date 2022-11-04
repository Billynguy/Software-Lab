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

## Documents in `Users` Collection

```json
{
    "$jsonSchema": {
        "required": ["username", "userid", "password", "projects"],
        "properties": {
            "username": {
                "bsonType": "string"
            },
            "userid": {
                "bsonType": "string"
            },
            "password": {
                "bsonType": "string"
            },
            "projects": {
                "bsonType": "array",
                "uniqueItems": true,
                "items": {
                    "bsonType": "string"
                },
                "description": "List of project ids."
            }
        }
    }
}
```

## Documents in `Projects` Collection

```json
{
    "$jsonSchema": {
        "required": ["projectid", "name", "description", "admin", "users", "hwsets"],
        "properties": {
            "projectid": {
                "bsonType": "string"
            },
            "name": {
                "bsonType": "string"
            },
            "description": {
                "bsonType": "string"
            },
            "admin": {
                "bsonType": "string",
                "description": "User id."
            },
            "users": {
                "bsonType": "array",
                "uniqueItems": true,
                "items": {
                    "bsonType": "string"
                },
                "description": "List of user ids."
            },
            "hwsets": {
                "bsonType": "object",
                "patternProperties": {
                    ".*": {
                        "bsonType": "int",
                        "minimum": 1
                    }
                },
                "description": "Map of hardware sets to the amount the project checked out."
            }
        }
    }
}
```

## Documents in `HWSet` Collection

```json
{
    "$jsonSchema": {
        "required": ["name", "userid", "password", "projects"],
        "properties": {
            "name": {
                "bsonType": "string"
            },
            "capacity": {
                "bsonType": "int",
                "minimum": 0
            },
            "availability": {
                "bsonType": "int",
                "minimum": 0
            },
            "projects": {
                "bsonType": "object",
                "patternProperties": {
                    ".*": {
                        "bsonType": "int",
                        "minimum": 1
                    }
                },
                "description": "Map of project ids to the amount they checked out."
            }
        }
    }
}
```
