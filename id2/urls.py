# -*- coding: utf-8 -*-

from django.conf.urls import patterns,url

from id2 import views

urlpatterns = patterns('',
        url(r'^$',views.index,name='index'),
        url(r'login/$',views.entree,name='entree'),
        url(r'logout/$',views.sortie,name='sortie'),
        url(r'login/verification/$',views.entreeVerification,name='entreeVerification'),

        url(r'inscription/$',views.inscription, name='inscription'),
        url(r'inscription/traitement/$',views.inscriptionTraitement,
            name='inscriptionTraitement'),

        url(r'visite/(?P<usager_id>\d+)/$',views.visite,name='visite'),
        url(r'visite/traitement/$',views.visiteTraitement,
            name='visite-traitement'),

        url(r'consigne/(?P<visite_id>\d+)/$',views.consignerDepart),
        url(r'consigne/traitement/(?P<visite_id>\d+)/$',
            views.consigneTraitement,\
                name="consigne-traitement"),

        url(r'service/(?P<service_id>\d+)/recherche/$',
            views.serviceRecherche,
            name='service-recherche'),
        url(r'service/recherche/traitement/$',
            views.serviceRechercheTraitement,
            name='service-recherche-traitement'),
        url(r'service/(?P<service_id>\d+)/(?P<abonne_id>\d+)/ajouter$',
            views.serviceAbonneAjout,
            name="service-abonne-ajout"),

        url(r'recherche/$',views.recherche, name='recherche'),
        url(r'recherche/traitement/$',views.rechercheTraitement,
            name='recherche-traitement'),
        )
