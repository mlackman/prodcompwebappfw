
class Status(object):

    def __init__(self):
        self.not_found = '404 Not Found'
        self.ok = '200 OK'

status = Status()


class HttpResponse(object):
    
    def __init__(self, status=None, data=None, headers=None):
        self.status = status
        self.data = data
        self.headers = headers or []

class HttpRequest(object):

    def __init__(self, path):
        self.path = path
