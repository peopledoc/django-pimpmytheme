from django.utils.functional import SimpleLazyObject
from django.contrib.sites.models import get_current_site


def get_site(request):
    return {
        'site': SimpleLazyObject(lambda: get_current_site(request)),
        }
