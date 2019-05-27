from smartmirror.glo_messages import GLO_MSG

GLO_CMD = {
    GLO_MSG['DISPLAY_WEATHER'] : 'pogoda',
    GLO_MSG['DISPLAY_DATE'] : 'data',
    GLO_MSG['DISPLAY_CLOCK'] : 'pokaż godzinę',
    GLO_MSG['HIDE_CLOCK'] : 'ukryj godzinę',
}

def GET_COMMAND(command):
    for _command_id, _command_str in GLO_CMD.items():
        if command == _command_str:
            return _command_id
    return None


if __name__ == '__main__':
    pass
