# -*- coding: utf-8 -*-

from django.conf.urls import url

from id2 import views

urlpatterns = [
        url(r'^$',views.index,name='index'),
        url(r'login/$',views.entree,name='entree'),
        url(r'logout/$',views.sortie,name='sortie'),
        url(r'login/verification/$',views.entreeVerification,name='entreeVerification'),

        url(r'inscription/$',views.inscription, name='inscription'),
        url(r'inscription/traitement/$',views.inscriptionTraitement,
            name='inscriptionTraitement'),

        url(r'visite/(?P<cat_visiteur>[a-z]+)/(?P<visiteur_id>\d+)/$',\
                views.visite,name='visite'),
        url(r'visite/traitement/$',views.visiteTraitement,
            name='visite-traitement'),


        url(r'consigne/traitement/(?P<cat_visiteur>[a-z]+)/(?P<visite_id>\d+)/$',
            views.consigneTraitement,\
                name="consigne-traitement"),
        url(r'consigne/(?P<cat_visiteur>[a-z]+)/(?P<visite_id>\d+)/$',\
                views.consignerDepart),

        url(r'service/recherche/traitement/$',
            views.serviceRechercheTraitement,
            name='service-recherche-traitement'),
        url(r'service/(?P<service_id>\d+)/abonnement/(?P<usager_id>\d+)/$',
            views.serviceAbonneAjout,
            name="service-abonne-ajout"),
        url(r'service/abonnement/traitement$',
            views.serviceAbonnementTraitement,
            name='service-abonnement-traitement'),
        url(r'service/abonnement/$',
            views.serviceAbonnement,
            name='service-index-traitement'),
        url(r'service/(?P<service_id>\d+)/$',
            views.serviceIndex,
            name='service-index'),

        url(r'recherche/$',views.recherche, name='recherche'),
        url(r'recherche/traitement/$',views.rechercheTraitement,
            name='recherche-traitement'),
        ]
