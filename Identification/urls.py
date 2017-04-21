# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    #url qui correspond a la page index du site
	url(r'^$', views.connexion, name='connexion'),
	#url qui correspond à la page de deconnexion
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
	#url correspond à la page d'accueil apres connexion de l'usager
    url(r'^home$', views.home, name='home'),
	#url correspond a la page enregistrement d'une visite et de usager
    url(r'^visiteusager$', views.visiteusager, name='visiteusager'),
    #url correspond à la page des statistiques par jour
	url(r'^jour$', views.home, name='jour'),
]
