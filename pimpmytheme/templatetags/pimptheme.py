from django import template
from django.conf import settings
from pimpmytheme.utils import get_lookup_class
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
register = template.Library()
project_name = settings.SETTINGS_MODULE.split(".")[0]


def pimp(context, file_type, filename=None):
    if filename is None:
        filename = ""
    lookup = get_lookup_class().objects.get_current()
    url = "/".join(
        [getattr(lookup, settings.CUSTOM_THEME_LOOKUP_ATTR),
         "static", file_type])
    url = "".join([context["STATIC_URL"], url, "/", filename])
    return url


@register.simple_tag(takes_context=True)
def pimp_css(context, filename=None):
    if pimp_exists(context, "css", filename=filename) is None:
        return ""
    else:
        return mark_safe("""<link rel="stylesheet" href="{}" type="text/css"
        media="screen" />""".format(pimp(context, "css", filename)))


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
    path = "/".join(
        [getattr(lookup, settings.CUSTOM_THEME_LOOKUP_ATTR),
         "static", filetype, filename])
    if finders.find(path) is None:
        return
    return pimp(context, filetype, filename)
