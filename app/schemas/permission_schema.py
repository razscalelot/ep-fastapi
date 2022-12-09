def permissionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "permission_name": item["permission_name"],
    }


def permissionsEntity(entity) -> list:
    return [permissionEntity(item) for item in entity]


def contentTypeEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "collection_name": item["collection_name"],
    }


def contentTypesEntity(entity) -> list:
    return [contentTypeEntity(item) for item in entity]


def userPermissionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "user_id": item["user_id"],
        "permission_id": item["permission_id"],
    }


def userPermissionsEntity(entity) -> list:
    return [userPermissionEntity(item) for item in entity]
