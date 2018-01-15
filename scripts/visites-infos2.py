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
    usagers_enreg = {}
    visit = {}
    for s in Service.objects.all():
        services.append(s.nom_serv)

    #Visite.objects.filter(date_arrivee__range=(mois[5][0],mois[5][1]))
    v_Total =\
            Visite.objects.filter(date_arrivee__range=(p[1][0],p[12][1]))
    for m in range(1,13):
        for v in services:
            v0 = v_Total.filter(service__nom_serv=v)
            visit[(v,m)] = []
            visit[(v,m)].append(v0.filter(\
                    date_arrivee__range=(p[m][0],p[m][1])))

    usagers_enreg = Usager.objects
        #visit[v] = (v0.count(),v0.values('usager').distinct().count())

    #Usager.objects.filter(visite__date_arrivee__range=(debut,maintenant))

    dacgl_stats = [usagers_enreg,visit,services]

    return dacgl_stats

#Usagers enregistrés

try :
    annee = int(sys.argv[1])
except IndexError:
    annee = datetime.now().year

stats = collecte(annee)

usager_Enregistre = stats[0].count()
Visites = stats[1]

from string import Template

skel =\
    """
    <tr>
     <td>${vTotal}</td><td>${vDistinct}</td>
    </tr>
    """
t = Template(skel)
# t.substitute(vTotal='',vDistinct='')

lieu = stats[2]
lieu.sort() #on trie par ordre alphabétique la liste des services
nbrservice = len(lieu)
skel_ligne = ''

for m in range(1,13):
    mois = m
    vTotalMois = 0
    skel_service = ''
    cellules = nbrservice
    premierTour = True
    for s in lieu:
        service = s
        v_par_service = Visites[s,m][0] #visite par service
        try:
            vTotal = v_par_service.count()
            vDistinct = v_par_service.values('usager').distinct().count()
        except IndexError:
            vTotal = 0
            vDistinct = 0

        vTotalMois += vDistinct
        if premierTour == True:
            skel_service =\
                    """
                    <td>{0}</td>
                        <td>{1}</td>
                        <td>{2}</td>
                        </tr>
                    """.format(service,
                        vTotal,
                        vDistinct,
                        )
            premierTour = False
        else :

            skel_service +=\
                    """
                    <tr>
                    <td>{0}</td>
                        <td>{1}</td>
                        <td>{2}</td>
                        </tr>
                    """.format(service,
                        vTotal,
                        vDistinct,
                        )

    skel_ligne += \
    """
    <tr>
    <td rowspan="{0}">{1}</td>
    {2}
    </tr>
    """.format(nbrservice,mois,skel_service)

tableau =\
"""
<table border=1>
 <tr>
  <th>Mois</th>
  <th>Service</th>
  <th>Nombre de visites au total</th>
  <th>Nombre de visites distinctes</th>
 </tr>
 {0}
</table>
""".format(skel_ligne)


#il faut dessiner le tableau

#    nbr = infosUsager[m].count()
#    skel +=\
#    """
#    <tr>
#     <td>{0}</td><td>{1}</td>
#    </tr>
#    """.format(m,nbr)

print (tableau)
