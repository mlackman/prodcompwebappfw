
class Status(object):

    def __init__(self):
        self.not_found = '404 Not Found'

status = Status()


class HttpResponse(object):
    
    def __init__(self, status=None, data=None, headers=None):
        self.status = status
        self.data = data
        self.headers = headers