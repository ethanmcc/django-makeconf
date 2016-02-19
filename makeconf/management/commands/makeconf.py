# deploy/management/commands/build.py

import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader


class InvalidVarException(object):
    def __mod__(self, missing):
        try:
            missing_str = unicode(missing)
        except:
            missing_str = 'Failed to create string representation'
        raise Exception('Unknown template variable {} {}'.format(missing,
                                                                 missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False


class Command(BaseCommand):
    help = 'Build Dockerfile and .ebextensions/ files'

    def render_template(self, source, dest, context):
        template = loader.get_template(source)
        output = template.render(context)
        self.stdout.write('Writing {0}'.format(dest))
        self.write_file(dest, output)

    def write_file(self, dest, output):
        if os.path.splitext(dest)[1] in self.executable_extensions:
            mode = int('0755', 8)
        else:
            mode = int('0644', 8)
        with os.fdopen(
                os.open(dest, os.O_TRUNC | os.O_WRONLY | os.O_CREAT, mode),
                'w') as file_:
            file_.write(output)

    def _get_template_map(self):
        try:
            map_ = settings.MAKECONF_MAP
        except AttributeError:
            map_ = {}
        try:
            eb_modules = settings.MAKECONF_EB_MODULES
            if os.path.isdir('.ebextensions'):
                self.stdout.write('Removing directory .ebextensions')
                shutil.rmtree('.ebextensions')
            for count, module in enumerate(eb_modules):
                key = '.ebextensions/{:02d}_{}.config'.format(count + 1,
                                                              module)
                map_[key] = '{}.tmpl'.format(module)
        except AttributeError:
            pass
        return map_

    def _create_basedirs(self, path):
        dirname = os.path.split(path)[0]
        if dirname:
            if os.path.exists(dirname):
                if dirname != '.ebextensions':
                    self.stdout.write('Directory {} exists'.format(dirname))
            else:
                self.stdout.write('Creating directory {}'.format(dirname))
                os.makedirs(dirname)

    def handle(self, *args, **options):
        settings.TEMPLATE_DEBUG = True
        settings.TEMPLATE_STRING_IF_INVALID = InvalidVarException()
        if not hasattr(settings, 'MAKECONF_OPTIONS'):
            settings.MAKECONF_OPTIONS = {}
        self.executable_extensions = settings.MAKECONF_OPTIONS.get(
            'executable_extensions', ['.sh'])

        context = {'settings': settings}
        self.stdout.write('context is: {}'.format(context))

        for path, template in sorted(self._get_template_map().items()):
            self._create_basedirs(path)
            self.render_template(template, path, context)
