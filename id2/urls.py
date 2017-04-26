# -*- coding: utf-8 -*-

from django.conf.urls import patterns,url

from id2 import views

urlpatterns = patterns('',
        url(r'^$',views.index,name='index'),
        url(r'login/$',views.entree,name='entree'),
        url(r'logout/$',views.sortie,name='sortie'),
        url(r'login/verification/$',views.entreeVerification,name='entreeVerification'),
        url(r'inscription/$',views.inscription, name='inscription'),
        url(r'inscription/traitement/$',views.inscriptionTraitement, name='inscriptionTraitement'),
        url(r'recherche/$',views.recherche, name='recherche'),
        url(r'recherche/traitement/$',views.rechercheTraitement,
            name='recherche-traitement'),
        url(r'visite/(?P<usager_id>\d+)/$',views.visite,name='visite'),
        url(r'visite/traitement/$',views.visiteTraitement, name='visite-traitement'),
        )
