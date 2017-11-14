#-*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = "inventaire2"

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^extraction',
            views.extraction, name='extraction'),
        url(r'^importation/csv',
            views.importation, name='importation'),
        url(r'^importation/traitement/csv',
            views.importationProcess, name='importation-process'),
        ]
