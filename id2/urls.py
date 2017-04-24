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
        )
