from smartmirror.glo_messages import GLO_MSG

GLO_CMD = {
    GLO_MSG['SHOW_WEATHER'] : 'pogoda',
    GLO_MSG['SHOW_DATE'] : 'data',
    GLO_MSG['SHOW_CLOCK'] : 'godzina',
}

def GET_COMMAND(command):
    for _command_id, _command_str in GLO_CMD.items():
        if command == _command_str:
            return _command_id
    return None

if __name__ == '__main__':
    pass