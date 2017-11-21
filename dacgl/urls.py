from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^login/$', views.entree,
        name='entree'),
    url(r'^logout/$', auth_views.logout,
        {'template_name':'dacgl/sortie.html'},
        name='sortie'),

    url(r'^$', views.home, name='home'),
    url(r'^manif/', include('manif.urls')),
    url(r'^inventaire2/', include('inventaire2.urls')),
    url(r'^ident/', include('id2.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
