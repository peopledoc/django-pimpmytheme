from django.contrib.sites.models import Site, SiteManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class PimpSiteManager(SiteManager):
    """ Pimp Site Manager """

    def get_current(self, **kwargs):
        kwargs.pop('context')
        return super(PimpSiteManager, self).get_current(**kwargs)


class PimpSite(models.Model):
    """ Custom Pimp Site """
    domain = models.CharField(_('domain name'), max_length=100)
    name = models.CharField(_('display name'), max_length=50)

    objects = PimpSiteManager()

    class Meta:
        db_table = 'django_site'
