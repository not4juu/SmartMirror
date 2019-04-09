GLO_MSG = {
'API_WINDOW_INITIALIZED' : 1,
'AUTHORIZATION_COMPLETE' : 2,
}


def GET_MESSAGE(message):
    for _message_str, _message_id in GLO_MSG.items():
        if message == _message_id:
            return _message_str
    return None