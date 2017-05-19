import os
import posixpath

from django.conf import settings as django_settings

from compressor.filters.css_default import CssAbsoluteFilter, SCHEMES


class PrefixedCssAbsoluteFilter(CssAbsoluteFilter):

    def _converter(self, matchobj, group, template):
        url = matchobj.group(group)

        url = url.strip()
        wrap = '"' if url[0] == '"' else "'"
        url = url.strip('\'"')

        if url.startswith('#'):
            return template % (wrap, url, wrap)
        elif url.startswith(SCHEMES):
            return template % (wrap, self.add_suffix(url), wrap)
        full_url = posixpath.normpath('/'.join([str(self.directory_name),
                                                url]))

        # custom
        partial_url = full_url[len(self.url) + 1:]
        if not os.path.isfile(
                os.path.join(
                    django_settings.STATIC_ROOT, partial_url)):
            dir_name = '/'.join((
                self.url,
                os.path.dirname(self.path)[len('/'.join([
                    django_settings.PIMPMYTHEME_FOLDER_NAME,
                    django_settings.SETTINGS_MODULE.split('.')[0]])) + 1:]))
            full_url = posixpath.normpath('/'.join([str(dir_name), url]))
        # end custom

        if self.has_scheme:
            full_url = "%s%s" % (self.protocol, full_url)
        return template % (wrap, self.add_suffix(full_url), wrap)
