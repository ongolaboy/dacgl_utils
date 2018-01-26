from django.conf.urls import patterns, include, url

urlpatterns = patterns('bureautique.views',
     url(r'^retrait/$', 'retrait'),
     url(r'^consommable/$', 'consommable'),
     url(r'^$', 'home'),
)
