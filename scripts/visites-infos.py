#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys

import django

from datetime import timedelta,date,datetime

from django.utils import timezone


"""
Collecter des données issues de ces visites
en fonction de la période indiquée

Récolter des informations suite à la saisie de toutes ces infos
et les envoyer par courriel
"""

BASE_DIR = '/home/willy/lab/django/dacgl_utils'
sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"


django.setup()

from dacgl.settings import TIME_ZONE
from id2.utils import periodes
from id2.models import Visite,Usager,Service

def collecte(annee):
    """
    Récupération des infos

     Pour chaque section
     * total
     * CNF
     * Fablab
     * Autres

    Nombre de visite ce mois
    Nombre de nouveaux inscrits

    """


    dacgl_stats = []
    p = periodes(annee)


    services = []
    for s in Service.objects.all():
        services.append(s.nom_serv)

    #Visite.objects.filter(date_arrivee__range=(mois[5][0],mois[5][1]))
    v_Total =\
            Visite.objects.filter(date_arrivee__range=(p[1][0],p[12][1]))
    visit = {}
    for v in services:
        v0 = v_Total.filter(service__nom_serv=v)
        visit[v] = []
        for m in range(1,13):
            visit[v].append(v0.filter(\
                    date_arrivee__range=(p[m][0],p[m][1])))
#       visit[v] = v0
        #visit[v] = (v0.count(),v0.values('usager').distinct().count())
    visit['TOTAL'] = (v_Total.count(),
            v_Total.values('usager').distinct().count()
            )

    usagers_enreg = {}
    for m in range(1,13):
        usagers_enreg[m] = Usager.objects.filter(\
                visite__date_arrivee__range=(p[m][0],p[m][1])
                )

    #Usager.objects.filter(visite__date_arrivee__range=(debut,maintenant))

    dacgl_stats = [usagers_enreg,visit]

    return dacgl_stats
