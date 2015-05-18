# deploy/management/commands/build.py

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader, Context
import os


class Command(BaseCommand):
    help = 'Build Dockerfile and .ebextensions/ files'

    def render_template(self, source, dest, context):
        template = loader.get_template(source)
        output = template.render(context)
        self.stdout.write('Writing {0}'.format(dest))
        with open(dest, 'w') as file:
            file.write(output)

    def _get_template_map(self):
        try:
            map_ = settings.MAKECONF_MAP
        except AttributeError:
            map_ = {}
        return map_

    def _create_basedirs(self, path):
        dirname = os.path.split(path)[0]
        if dirname:
            if os.path.exists(dirname):
                self.stdout.write('Directory {} exists'.format(dirname))
            else:
                self.stdout.write('Creating directory {}'.format(dirname))
                os.makedirs(dirname, exist_ok=True)

    def handle(self, *args, **options):
        context = Context({'settings': settings})
        self.stdout.write('context is: {}'.format(context))

        for path, template in self._get_template_map().items():
            self._create_basedirs(path)
            self.render_template(template, path, context)
