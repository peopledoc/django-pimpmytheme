from django import template
from django.conf import settings
from pimpmytheme.utils import get_lookup_class
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
from django.templatetags.static import static
register = template.Library()
project_name = settings.SETTINGS_MODULE.split(".")[0]


@register.simple_tag(takes_context=True)
def pimp(context, file_type, filename=None):

    if filename is None:
        filename = ""
    lookup = get_lookup_class().objects.get_current()

    # lookup is not mandatory, maybe we do not have current item right now.
    if not lookup:
        return '#'

    paths = []
    if hasattr(settings, 'PIMPMYTHEME_FOLDER_NAME'):
        paths = [settings.PIMPMYTHEME_FOLDER_NAME, project_name]

    paths.extend([getattr(lookup, settings.CUSTOM_THEME_LOOKUP_ATTR),
                  "static", file_type])
    url = "/".join(paths)
    url = static("".join([url, "/", filename]))
    return url


@register.simple_tag(takes_context=True)
def pimp_css(context, filename=None, css_type=None):
    if css_type is None:
        css_type = "css"
    if pimp_exists(context, "css", filename=filename) is None:
        return ""
    else:
        return mark_safe("""<link rel="stylesheet" href="{}" type="text/{}"
        media="screen" />""".format(pimp(context, "css", filename), css_type))


@register.simple_tag(takes_context=True)
def pimp_js(context, filename=None):
    if pimp_exists(context, "js", filename=filename) is None:
        return ""
    else:
        return mark_safe(
            """<script type="text/javascript" src="{}"></script>""".format(
                pimp(context, "js", filename)))


@register.simple_tag(takes_context=True)
def pimp_img(context, filename=None):
    if pimp_exists(context, "img", filename=filename) is None:
        return ""
    else:
        return mark_safe(
            """<img src="{}" />""".format(
                pimp(context, "img", filename)))


def pimp_exists(context, filetype, filename=None):
    if filename is None:
        filename = ""
    lookup = get_lookup_class().objects.get_current()

    # lookup is not mandatory, maybe we do not have current item right now.
    if not lookup:
        return

    paths = []
    if hasattr(settings, 'PIMPMYTHEME_FOLDER_NAME'):
        paths = [settings.PIMPMYTHEME_FOLDER_NAME, project_name]
    paths.extend([getattr(lookup, settings.CUSTOM_THEME_LOOKUP_ATTR),
                  "static", filetype, filename])
    path = "/".join(paths)
    if finders.find(path) is None:
        return
    return pimp(context, filetype, filename)
