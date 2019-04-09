GLO_MSG = {
'NO_ERROR' : 0,
'API_WINDOW_INITIALIZED' : 1,
'API_CAMERA_CONNECTION_FAILURE' : 2,
'API_USER_QUIT' : 3,
'AUTHORIZATION_COMPLETE' : 4,

}


def GET_MESSAGE(message):
    for _message_str, _message_id in GLO_MSG.items():
        if message == _message_id:
            return _message_str
    return None