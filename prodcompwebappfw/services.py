import re

class Filesystem(object):

    def read(self, filename):
        with open(filename, 'rt') as f:
            return f.read()

class MimeType(object):

    def __init__(self, type, is_text_type):
        self.type = type
        self.is_text_type = is_text_type

    def __str__(self):
        return self.type

class MimeTypeResolver(object):

    # filename extension, mime_type, is_text_type
    mime_types = [
        ('.html', 'text/html', True), ('.css', 'text/css', True), 
        ('.js', 'application/javascript', True), ('.jpg', 'image/jpeg', False), 
        ('.png', 'image/png', False)
    ]

    def get_type(self, filename):
        for file_extension, mime_type, is_text_type in MimeTypeResolver.mime_types:
            if filename.endswith(file_extension):
                return MimeType(mime_type, is_text_type)
        return 'text/plain'

class ContentEncoder(object):

    def encode(self, content, encoding):
        return content.encode(encoding)


