GLO_CMD = {
    'SHOW_WEATHER' : 'pokaż pogodę',
    'SHOW_DATE' : 'pokaż datę',
}

def GET_COMMAND(command):
    for _command_str, _command_id in GLO_CMD.items():
        if command == _command_id:
            return _command_str
    return None

if __name__ == '__main__':
    pass