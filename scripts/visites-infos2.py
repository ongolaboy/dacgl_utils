# -*- coding:utf-8 -*-
"""
Collecter des données issues des visites pour une année.

Exemple d'usage
"python3 visites-infos2.py [annee] [mois] [courriel]"

L'année peut être donnée en paramètre au si elle est absente
le script considèrera l'année en cours.

Le mois si fourni, le script ne ressortira que les infos du mois
indiqué. Nombre entre 1-12

'courriel' doit être  écrit tel quel.

En sortie le script génère un fichier au format html contenant un
tableau. Ce dernier pourra aussi être envoyé par courriel.
"""


import os
import sys
import email
import smtplib

import django

from datetime import timedelta,date,datetime
from pytz import timezone as tzone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template

from django.utils import timezone

from conf import *



sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"


django.setup()

from dacgl.settings import TIME_ZONE
from id2.utils import periodes,collecte
from id2.models import Visite,Usager,Service

#on récupère l'année fournie en paramètre le cas échéant
try :
    annee = int(sys.argv[1])
except IndexError:
    annee = datetime.now().year

#éventuellement aussi le mois
try :
    mois = int(sys.argv[2])
    #pour le moment on appelle ce fichier via un script et par défaut
    #on veut les infos sur le mois précédent
    #TODO à améliorer
    if mois == 1:
        mois = 12
        annee -= 1
    else:
        mois -= 1
except IndexError:
    mois = ''
try :
    expedition = sys.argv[3]
except IndexError:
    expedition = None


def envoiStats(s_smtp,from_addr,to_addrs,sujet,TIME_ZONE,msg_utils):
    """
    Envoi des stats à une liste interne.
    """

    moment = datetime.now(tzone(TIME_ZONE)).\
        strftime('%a, %d %B %Y %H:%M:%S %z')
    #create message container

    msg =  MIMEMultipart('alternative')
    msg['Subject'] = sujet
    msg['From'] = from_addr
    msg['To'] = to_addrs
    msg['Date'] = moment

    #create the body of the message
    message = u"""
    Veuillez activer l'affichage HTML svp
    en attendant que nous formations correctement en
    mode texte
    """

    message_html = msg_utils

    #record the MIME types
    part1 = MIMEText(message, 'plain')
    part2 = MIMEText(message_html, 'html')

    #attach parts into message container
    msg.attach(part1)
    msg.attach(part2)

    #send
    client = smtplib.SMTP(s_smtp)
    try:
            client.sendmail(from_addr,to_addrs,msg.as_string())
            return 'stats fréquentations mensuelles envoyées'
    except Exception:
        return "Oups :-("


stats = collecte(annee,mois)

usager_Enregistre = stats[0].count()
usager_Enregistre_H = stats[0].filter(sexe='H').count()
usager_Enregistre_F = stats[0].filter(sexe='F').count()
Visites = stats[1]


lieu = stats[2]
lieu.sort() #on trie par ordre alphabétique la liste des services
nbrservice = len(lieu)
skel_ligne = ''
tableau_brique1 =\
            """
    <td>{0}</td>
        <td style="text-align:center">{1}</td>
        <td style="text-align:center">{2} <br /><p style="font-size:smaller">Dont  <em>{3} Femmes et {4} Hommes</em></p></td>
        </tr>
                """
tableau_brique2 =\
"""
    <tr>
    {0}
""".format(tableau_brique1)
affichage_mois = ''
premierTour = True #pour distinguer la première colonne des autres
sujet = "Informations sur les visites au {0}: ".format(SITE)
sujet_annuel = "{0} Année {1}".format(sujet,annee)
sujet_mensuel = "{0} période {1}/{2}".format(sujet,annee,mois)

if mois != '':
    sujet = sujet_mensuel
    affichage_mois = '<p>Mois:{0}</p>'.format(mois)
    vTotalMois = 0
    skel_service = ''
    cellules = nbrservice
    for s in lieu:
        service = s
        v_par_service = Visites[s,mois][0] #visite par service
        try:
            vTotal = v_par_service.count()
            vDistinct = v_par_service.values('usager').distinct().count()
            vDistinct_H = v_par_service.values('usager').distinct().\
                    filter(usager__sexe='H').count()
            vDistinct_F = v_par_service.values('usager').distinct().\
                    filter(usager__sexe='F').count()
        except IndexError:
            vTotal = 0
            vDistinct = 0

        vTotalMois += vDistinct
        if premierTour == True:
            skel_service = tableau_brique1.format(service,
                        vTotal,
                        vDistinct,
                        vDistinct_F,
                        vDistinct_H,
                        )
            premierTour = False
        else :

            skel_service += tableau_brique2.format(service,
                        vTotal,
                        vDistinct,
                        vDistinct_F,
                        vDistinct_H,
                        )

    skel_ligne += \
    """
    <tr>
    <td rowspan="{0}">{1}</td>
    {2}
    </tr>
    """.format(nbrservice,mois,skel_service)

else :
    sujet = sujet_annuel
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
                vDistinct = v_par_service.values('usager').distinct().\
                        count()
                vDistinct_H = v_par_service.values('usager').distinct().\
                        filter(usager__sexe='H').count()
                vDistinct_F = v_par_service.values('usager').distinct().\
                        filter(usager__sexe='F').count()
            except IndexError:
                vTotal = 0
                vDistinct = 0

            vTotalMois += vDistinct
            if premierTour == True:
                skel_service = tableau_brique1.format(service,
                            vTotal,
                            vDistinct,
                            vDistinct_F,
                            vDistinct_H,
                            )
                premierTour = False
            else :

                skel_service +=tableau_brique2.format(service,
                            vTotal,
                            vDistinct,
                            vDistinct_F,
                            vDistinct_H,
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
<!DOCTYPE html>
<html>

  <head>
   <meta http-equiv="content-type" content="text/html; charset=utf-8" />
   <title> Stats sur la fréquentation - {0}</title>
  </head>

  <body>
    <h2> Année {1} </h2>
     <a href="{4}">{4}</a>
    {5}
    <p>Nombre total d'usagers enregistrés toute période confondue: {2}.
    <br />Dont:
    <ul>
     <li>{6} Femmes</li>
     <li>{7} Hommes</li>
    </ul>
    <br />
    {3}
  </body>
</html>
    """.format(SITE,annee,usager_Enregistre,tableau,
            ACCUEIL,affichage_mois,
            usager_Enregistre_F,
            usager_Enregistre_H)

print (skel0)
#doit-on expédier,afficher les résultats ?
if expedition == 'courriel':
    msg_utils = skel0
    envoiStats(s_smtp,from_addr,to_addrs,sujet,TIME_ZONE,msg_utils)
