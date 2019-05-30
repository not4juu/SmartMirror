from smartmirror.glo_messages import GLO_MSG

"""
    ApiState Class
"""


class ApiState(object):
    def __init__(self):
        self.__api_runs = True
        self.__api_info = GLO_MSG['NO_ERROR']

    @property
    def api_runs(self):
        return self.__api_runs

    @api_runs.setter
    def api_runs(self,api_state):
        self.__api_runs = api_state

    @property
    def api_info(self):
        return self.__api_info

    @api_info.setter
    def api_info(self, api_info):
        self.__api_info = api_info


if __name__ == '__main__':
    pass
