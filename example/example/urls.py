from django.conf.urls import include
from django.conf.urls import url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', 'subapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
