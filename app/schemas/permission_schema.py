def permissionEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "permission_name": item["permission_name"],
    }


def permissionsEntity(entity) -> list:
    return [permissionEntity(item) for item in entity]
