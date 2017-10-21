from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #url(r'^$', 'dacgl.views.home', name='home'),
    url(r'^ident/', include('id2.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
