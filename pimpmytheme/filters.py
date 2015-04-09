import os
import posixpath
import re

from compressor.filters.css_default import CssAbsoluteFilter

URL_PATTERN = re.compile(r'url\(([^\)]+)\)')
SRC_PATTERN = re.compile(r'src=([\'"])(.+?)\1')
SCHEMES = ('http://', 'https://', '/', 'data:')

from django.conf import settings as django_settings


class PrefixedCssAbsoluteFilter(CssAbsoluteFilter):

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
                    django_settings.STATIC_ROOT, full_url[len(self.url)+1:])):
            dir_name = '/'.join((
                self.url,
                os.path.dirname(self.path)[len('/'.join([
                    django_settings.PIMPMYTHEME_FOLDER_NAME,
                    django_settings.SETTINGS_MODULE.split('.')[0]]))+1:]))
            full_url = posixpath.normpath('/'.join([str(dir_name), url]))

        if self.has_scheme:
            full_url = "%s%s" % (self.protocol, full_url)
        return template % self.add_suffix(full_url)
