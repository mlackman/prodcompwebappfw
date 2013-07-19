import jinja2

class Renderer(object):

    def __init__(self, templates_path):
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))

    def render(self, template_name, **kwargs):
        template = self._env.get_template(template_name)
        return template.render(kwargs)