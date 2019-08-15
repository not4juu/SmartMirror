from smartmirror.glo_messages import GLO_MSG

GLO_CMD = {
    GLO_MSG['DISPLAY_WEATHER']: 'pokaż pogodę',
    GLO_MSG['HIDE_WEATHER']: 'ukryj pogodę',
    GLO_MSG['DISPLAY_NEWS']: 'pokaż wiadomości',
    GLO_MSG['HIDE_NEWS']: 'ukryj wiadomości',
    GLO_MSG['DISPLAY_CLOCK']: 'pokaż zegar',
    GLO_MSG['HIDE_CLOCK']: 'ukryj zegar',
    GLO_MSG['LOGOUT']: 'wyloguj',
}


def GET_COMMAND(command):
    for _command_id, _command_str in GLO_CMD.items():
        if command == _command_str:
            return _command_id
    return None


if __name__ == '__main__':
    pass
