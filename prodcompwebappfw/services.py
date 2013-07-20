import re

class Filesystem(object):

    def read(self, filename):
        with open(filename, 'rt') as f:
            return f.read()

class MimeTypeResolver(object):

    mime_types = [
        ('.html', 'text/html'), ('.css', 'text/css'), ('.js', 'application/javascript'),
        ('.jpg', 'image/jpeg'), ('.png', 'image/png')
    ]

    def get_type(self, filename):
        for file_extension, mime_type in MimeTypeResolver.mime_types:
            if filename.endswith(file_extension):
                return mime_type
        return 'text/plain'


