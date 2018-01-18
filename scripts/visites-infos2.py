# -*- coding:utf-8 -*-
"""
Collecter des données issues des visites pour une année.

Exemple d'usage
"python3 visites-infos2.py [annee] [mois]"

L'année peut être donnée en paramètre au si elle est absente
le script considèrera l'année en cours.

Le mois si fourni, le script ne ressortira que les infos du mois
indiqué. Nombre entre 1-12

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
except IndexError:
    mois = ''


def envoiStats(s_smtp,from_addr,to_addrs,sujet,TIME_ZONE,msg_utils):
    """
    Envoi des stats à une liste interne
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
Visites = stats[1]


lieu = stats[2]
lieu.sort() #on trie par ordre alphabétique la liste des services
nbrservice = len(lieu)
skel_ligne = ''
affichage_mois = ''
premierTour = True #pour distinguer la première colonne des autres
sujet = "Informations sur les visites au {0}: ".format(SITE)
sujet_annuel = "{0} Annee {1}".format(sujet,annee)
sujet_mensuel = "{0} Mois: {1}".format(sujet,mois)

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
<!DOCTYPE html>
<html>

  <head>
   <meta http-equiv="content-type" content="text/html; charset=utf-8" />
   <title> Stats sur la frequentation - {0}</title>
  </head>

  <body>
    <h2> Année {1} </h2>
    {4}
    {5}
    <p>Nombre total d'usagers enregistrés toute période confondue: {2}
    <br />
    {3}
  </body>
</html>
    """.format(SITE,annee,usager_Enregistre,tableau,
            ACCUEIL,affichage_mois)

#sortie = Template(skel0)
#TODO à présenter ainsi plus tard quand ça sera ok
#sortie.substitute(IMPLANTATION=SITE,
#        STATISTIQUES=tableau)

print (skel0)
#envoi courriel

#envoiStats(s_smtp,from_addr,to_addrs,sujet,TIME_ZONE,msg_utils)
