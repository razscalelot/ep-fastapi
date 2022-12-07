from fastapi.responses import JSONResponse
from fastapi import status


def onSuccess(message, result):
    return JSONResponse({
        "Message": message,
        "Data": result,
        "Status": status.HTTP_200_OK,
        "IsSuccess": True
    })


def onError(error):
    return JSONResponse({
        "Message": error.message,
        "Data": 0,
        "Status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "IsSuccess": False
    })


def unauthorisedRequest():
    return JSONResponse({
        "Message": "Unauthorized Request!",
        "Data": 0,
        "Status": status.HTTP_401_UNAUTHORIZED,
        "IsSuccess": False
    })


def forbiddenRequest():
    return JSONResponse({
        "Message": "Access to the requested resource is forbidden! Contact Administrator.",
        "Data": 0,
        "Status": status.HTTP_403_FORBIDDEN,
        "IsSuccess": False
    })


def badRequest(message):
    return JSONResponse({
        "Message": message,
        "Data": 0,
        "Status": status.HTTP_400_BAD_REQUEST,
        "IsSuccess": False
    })
