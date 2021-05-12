import os
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
