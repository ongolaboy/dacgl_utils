# -*- coding:utf-8 -*-
"""
Collecter des données issues des visites pour une année.

Exemple d'usage
"python3 visites-infos2.py <annee>"

L'année peut être donnée en paramètre au si elle est absente
le script considèrera l'année en cours.
En sortie le script génère un fichier au format html contenant un
tableau. Ce dernier pourra aussi être envoyé par courriel.
"""


import os
import sys

import django

from datetime import timedelta,date,datetime
from string import Template

from django.utils import timezone



BASE_DIR = '/home/willy/lab/django/dacgl_utils'
SITE = 'Bureau régional'
sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"


django.setup()

from dacgl.settings import TIME_ZONE
from id2.utils import periodes
from id2.models import Visite,Usager,Service

def collecte(annee,mois=''):
    """
    Collecte des données sur une année donnée

    La sortie est une liste contenant:

    * le nombre d'usagers enregistrées sur l'année

    * les infos sur les visites
     * elles sont présentées par service dans un dictionnaire
       où les clés des tuples (service,mois)
       ex: visite[('CNF',11)] renvoie un querySet correspondant
       aux visites effectuées dans le CNF en Novembre

    * la liste des services
    """


    dacgl_stats = []
    p = periodes(annee,mois)


    services = []
    usagers_enreg = {}
    visit = {}
    for s in Service.objects.all():
        services.append(s.nom_serv)

    v_Total =\
            Visite.objects.filter(date_arrivee__range=(p[1][0],p[12][1]))
    for m in range(1,13):
        for v in services:
            v0 = v_Total.filter(service__nom_serv=v)
            visit[(v,m)] = []
            visit[(v,m)].append(v0.filter(\
                    date_arrivee__range=(p[m][0],p[m][1])))

    usagers_enreg = Usager.objects

    dacgl_stats = [usagers_enreg,visit,services]

    return dacgl_stats

#Commençons donc à collecter les infos

#on récupère l'année fournie en paramètre le cas échéant
try :
    annee = int(sys.argv[1])
except IndexError:
    annee = datetime.now().year

stats = collecte(annee)

usager_Enregistre = stats[0].count()
Visites = stats[1]


lieu = stats[2]
lieu.sort() #on trie par ordre alphabétique la liste des services
nbrservice = len(lieu)
skel_ligne = ''

for m in range(1,13):
    mois = m
    vTotalMois = 0
    skel_service = ''
    cellules = nbrservice
    premierTour = True #pour distinguer la première colonne des autres
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

#Les ossatures
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

skel0 =\
    """
<html>

  <head>
   <title> Stats sur la frequentation - {0}</title>
  </head>

  <body>
    <h2> Année {1} </h2>
    <p>Nombre d'usagers enregistrés au total dans l'année: {2}
    <br />
    {3}
  </body>
</html>
    """.format(SITE,annee,usager_Enregistre,tableau)

#sortie = Template(skel0)
#TODO à présenter ainsi plus tard quand ça sera ok
#sortie.substitute(IMPLANTATION=SITE,
#        STATISTIQUES=tableau)

print (skel0)
