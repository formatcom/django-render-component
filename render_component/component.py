import re
from django.template import Context


class TemplateComponent:
    _render = None

    def __init__(self, name, template):
        self.name = name
        self.template = template
        self._pattern = re.compile(f'<{self.name}(?P<props>[\s\S]*?)>(?P<content>[\s\S]*?)<\/{self.name}>')

    @property
    def pattern(self):
        return self._pattern

    def render(self, source):
        if self.template.source == str(source):
            return self._render

        element = self.pattern.search(source)

        if not element:
            return source

        props = element.group('props').split()
        content = element.group('content')

        context = {}
        context['content'] = content

        for prop in props:
            key, value = prop.split('=')
            context[key] = re.sub(r'[\'|\"]', '', value)

        self._render = self.template.render(Context(context))
        return self._render
