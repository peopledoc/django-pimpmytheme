import os
import re
import posixpath

from compressor.filters.css_default import CssAbsoluteFilter

URL_PATTERN = re.compile(r'url\(([^\)]+)\)')
SRC_PATTERN = re.compile(r'src=([\'"])(.+?)\1')
SCHEMES = ('http://', 'https://', '/', 'data:')

from django.conf import settings as django_settings


class CustomCssAbsoluteFilter(CssAbsoluteFilter):

    def input(self, filename=None, basename=None, **kwargs):
        if not filename:
            return self.content
        self.path = basename.replace(os.sep, '/')
        self.path = self.path.lstrip('/')
        if self.url.startswith(('http://', 'https://')):
            self.has_scheme = True
            parts = self.url.split('/')
            self.url = '/'.join(parts[2:])
            self.url_path = '/%s' % '/'.join(parts[3:])
            self.protocol = '%s/' % '/'.join(parts[:2])
            self.host = parts[2]
        self.directory_name = '/'.join((
            self.url,
            django_settings.PIMPMYTHEME_FOLDER_NAME,
            django_settings.SETTINGS_MODULE.split('.')[0],
            os.path.dirname(self.path)))
        return SRC_PATTERN.sub(
            self.src_converter,
            URL_PATTERN.sub(self.url_converter, self.content))

    def _converter(self, matchobj, group, template):
        url = matchobj.group(group)
        url = url.strip(' \'"')
        if url.startswith('#'):
            return "url('%s')" % url
        elif url.startswith(SCHEMES):
            return "url('%s')" % self.add_suffix(url)
        full_url = posixpath.normpath('/'.join([str(self.directory_name),
                                                url]))

        if not os.path.isfile(
                os.path.join(
                    django_settings.STATIC_ROOT,
                    full_url[len(self.url)+1:])):
            dir_name = '/'.join((self.url, os.path.dirname(self.path)))
            full_url = posixpath.normpath('/'.join([str(dir_name), url]))

        if self.has_scheme:
            full_url = "%s%s" % (self.protocol, full_url)
        return template % self.add_suffix(full_url)
