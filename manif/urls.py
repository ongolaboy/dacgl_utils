from django.conf.urls import url

from . import views

app_name = 'manif'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^consigne/traitement/$', views.consigneTraitement,
            name='consigne-traitement'),
        url(r'^recherche/traitement/$', views.rechercheTraitement,
            name='recherche-traitement'),
        url(r'^consigne21', views.consigne21, name='consigne21'),
        url(r'^consigne/usager/(?P<user_id>\d+)',
            views.consigneUsager,
            name='consigneUsager'),
        url(r'^consigne', views.consigne, name='consigne'),
        url(r'^bilan/(?P<bilan_id>\d+)', views.bilanDetaille,
            name='bilan-detaille'),
        url(r'^bilan', views.bilan, name='bilan'),
        ]
