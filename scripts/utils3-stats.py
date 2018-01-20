#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import email
import smtplib

import django

from datetime import timedelta,date,datetime
from pytz import timezone as tzone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.utils import timezone

from conf import *


"""
Collecter des données issues de ces visites

Récolter des informations suite à la saisie de toutes ces infos
et les envoyer par courriel
"""

#collecte des stats
sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"


django.setup()

from dacgl.settings import TIME_ZONE
from id2.models import Visite,Usager


semaine_courante = date.today().isocalendar()[1]
date_jour = date.today()
fuseau = timezone.now()
debut_semaine = (fuseau - timedelta(days=fuseau.weekday())).\
        replace(hour=0,minute=0)

visit_semaine = Visite.objects.filter(date_arrivee__gte=debut_semaine)
service = ['CNF','fablab']
visit_service = {}
for svce in service:
    visit_service[svce] = visit_semaine.filter(service__nom_serv=svce)

usager_total = Usager.objects.count()

# section envoi courriel

to_addrs = 'willy.manga@auf.org'
sujet = 'Informations sur les visites à la DACGL: semaine {0}'.\
        format(semaine_courante)

moment = datetime.now(tzone(TIME_ZONE)).\
    strftime('%a, %d %B %Y %H:%M:%S %z')
#create message container

msg =  MIMEMultipart('alternative')
msg['Subject'] = sujet
msg['From'] = from_addr
msg['To'] = to_addrs
msg['Date'] = moment

#create the body of the message
message = """
Fréquence des visites à la DACGL pour la semaine courante:\n
Date du jour : {0} \n
 * Total de visites pour tout le bureau: {1}\n
  * Visites au CNF : {2}\n
  * Visites au Fablab: {3}\n

 * Nombre d'usagers enregistrés au total toute période: {4}\

Détails à l'adresse {5}.
         """.format(date_jour,visit_semaine.count(),
                 visit_service['CNF'].count(),
                 visit_service['fablab'].count(),
                 usager_total,
                 ACCUEIL_URL,
                 )

message_html = """\
        <html>
        <head><title>STATS - Bureau régional</title></head>
        <body>
         <h3>Frequence des visites à la DACGL pour la semaine courante</h3>
          <p>Date du jour: {0} </p>
        <ul>
         <li>Total des visites pour tout le bureau: {1}</li>
             <li>Visites au CNF: {2}</li>
             <li>Visites au fablab: {3}</li>
         <li>Total des usagers enregistrés toute période: {4}</li>
        </ul>
        <p>Details à l'adresse <a href="{5}">
        {5}</a>.
        </body>
        </html>
        """.format(date_jour,visit_semaine.count(),
                 visit_service['CNF'].count(),
                 visit_service['fablab'].count(),
                 usager_total,
                 ACCUEIL_URL,
                 )

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
        print ('stats fréquentations DACGL envoyées')
except Exception:
    print ("Oups :-(")
