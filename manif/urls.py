from django.conf.urls import url

from . import views

app_name = 'manif'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^consigne/traitement/$', views.consigneTraitement,
            name='consigne-traitement'),
        url(r'^consigne', views.consigne, name='consigne'),
        url(r'^bilan', views.bilan, name='bilan'),
        ]
