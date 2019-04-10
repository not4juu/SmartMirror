GLO_MSG = {
'NO_ERROR' : 0,
'API_WINDOW_INITIALIZED' : 1,
'NETWORK_CONNECTION_SUCCESS' : 2,
'NETWORK_CONNECTION_FAILURE' : 3,
'API_CAMERA_CONNECTION_FAILURE' : 4,
'API_USER_QUIT' : 5,
'AUTHORIZATION_COMPLETE' : 6,

}


def GET_MESSAGE(message):
    for _message_str, _message_id in GLO_MSG.items():
        if message == _message_id:
            return _message_str
    return None