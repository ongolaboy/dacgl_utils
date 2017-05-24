#!/usr/bin/python
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

"""
Collecter des données issues de ces visites
à l'échelle du mois.

Récolter des informations suite à la saisie de toutes ces infos
et les envoyer par courriel
"""

BASE_DIR = '/home/willy/dacgl'
sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"

from id2.models import Visite,Usager

django.setup()

def collecte():
    """
    Récupération des infos

     Pour chaque section
     * total
     * CNF
     * Fablab
     * Autres

    Nombre de visite ce mois
    Nombre de nouveaux inscrits

    Le script sera lancé le 1er jour du mois suivant.
    """

    dacgl_stats = {}


    debut0 = datetime.now(tz=timezone.get_current_timezone())
    debut = debut0.replace(month=debut0.month-1,
            day = 1,
            hour = 0,
            minute = 0,
            )
    #pour la fin , on cherche d'abord le dernier jour
    #ensuite on va à 23h
    fin = (debut0 - timedelta(days=debut0.day)).replace(hour=23)
    visit_mois = Visite.objects.filter(date_arrivee__range=(debut,fin))

    semaine_courante = date.today().isocalendar()[1]
    date_jour = date.today()
    mois_prec = date_jour.replace(month=
    fuseau = timezone.now()
    debut_semaine = (fuseau - timedelta(days=fuseau.weekday())).\
            replace(hour=0,minute=0)

    visit_semaine = Visite.objects.filter(date_arrivee__gte=debut_semaine)
    service = ['CNF','fablab']
    visit_service = {}
    for svce in service:
        visit_service[svce] = visit_semaine.filter(service__nom_serv=svce)

    usager_total = Usager.objects.all().count()

    return dacgl_stats

# section envoi courriel

s_smtp = "smtp.cm.auf.org"
from_addr = u'technique@cm.auf.org'
to_addrs = 'cnfy@cm.auf.org,ongolafablab@cm.auf.org'
sujet = 'Informations sur les visites a la DACGL: semaine %s' % \
        semaine_courante

moment = datetime.now(tzone('Africa/Douala')).\
    strftime('%a, %d %B %Y %H:%M:%S %z')
#create message container

msg =  MIMEMultipart('alternative')
msg['Subject'] = sujet
msg['From'] = from_addr
msg['To'] = to_addrs
msg['Date'] = moment

#create the body of the message
message = u"""
Frequence des visites a la DACGL pour la semaine courante:\n
Date du jour : %s \n
 * Total de visites : %s\n
  * Visites au CNF : %s\n
  * Visites au Fablab: %s\n

 * Nombre d'usagers enregistres au total : %s\

Details a l'adresse http://utils2.cm.auf.org/.
         """ % (date_jour,visit_semaine.count(),
                 visit_service['CNF'].count(),
                 visit_service['fablab'].count(),
                 usager_total,
                 )

message_html = """\
        <html>
        <head><title>Test</title></head>
        <body>
         <h3>Frequence des visites a la DACGL pour la semaine courante</h3>
          <p>Date du jour: %s </p>
        <ul>
         <li>Total des visites: %s</li>
             <li>Visites au CNF: %s</li>
             <li>Visites au fablab: %s</li>
         <li>Total des usagers enregistres: %s</li>
        </ul>
        <p>Details a l'adresse <a href="http://utils2.cm.auf.org/">
        http://utils2.cm.auf.org/</a>.
        </body>
        </html>
        """ % (date_jour,visit_semaine.count(),
                 visit_service['CNF'].count(),
                 visit_service['fablab'].count(),
                 usager_total,
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
        print 'stats fréquentations DACGL envoyées'
except Exception, err:
    print "Oups :-("
