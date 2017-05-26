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

    from django.db.models import Count

    dacgl_stats = []


    t_actuel = datetime.now(tz=timezone.get_current_timezone())
    t_debut_mois_prec = t_actuel.replace(month=t_actuel.month-1,
            day = 1,
            hour = 0,
            minute = 0,
            )
    #pour la fin , on cherche d'abord le dernier jour
    #ensuite on va à 23h
    t_fin_mois_prec = (t_actuel - timedelta(days=t_actuel.day)).\
            replace(hour=23)
    visit_mois_prec = Visite.objects.filter(date_arrivee__range=\
            (t_debut_mois_prec,t_fin_mois_prec))

    services = []
    for s in Service.objects.all():
        services.append(s.nom_serv)

    visit = {}
    for v in services:
        visit[v] = visit_mois_prec.filter(service__nom_serv=v).count()
    visit['TOTAL'] = visit_mois_prec.count()

    usagers_enreg = {}
    usagers_enreg['TOTAL'] = Usager.objects.count()
    usagers_enreg['Courant'] = Usager.objects.filter(\
            visite__date_arrivee__range=\
            t_debut_mois_prec,t_fin_mois_prec).count()

    #Usager.objects.annotate(nbr_visit=Count('visite'))
    #Usager.objects.filter(visite__date_arrivee__range=(debut,maintenant))

    dacgl_stats = [usagers_enreg,visit]

    return dacgl_stats

# section envoi courriel

def envoiStats(s_smtp,from_addr,to_addrs,sujet,fuseau,dacgl_stats):
    """
    Envoi des stats à une liste interne
    """

    moment = datetime.now(tzone(fuseau)).\
        strftime('%a, %d %B %Y %H:%M:%S %z')
    #create message container

    msg =  MIMEMultipart('alternative')
    msg['Subject'] = sujet
    msg['From'] = from_addr
    msg['To'] = to_addrs
    msg['Date'] = moment

    #create the body of the message
    message = u"""
    Statistiques des visites a la DACGL pour le mois de %s:\n

    = Nombre d'usagers enregistrés = \n
     * Au total : %s \n
     * Pour le mois: %s\n

    = Nombre de visites enregistrées = \n

    Details a l'adresse http://utils2.cm.auf.org/.
             """ % (dacgl_stats[usagers_enreg['TOTAL']],
                     dacgl_stats[usagers_enreg['Courant']],
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
            return 'stats fréquentations mensuelles DACGL envoyées'
    except Exception, err:
        return "Oups :-("


fuseau = 'Africa/Douala'
s_smtp = "smtp.cm.auf.org"
from_addr = u'technique@cm.auf.org'
to_addrs = 'diffusion-bureau@cm.auf.org'
sujet = 'Informations sur les visites a la DACGL: Mois de %s' % \
        (t_debut_mois_prec.strftime(%B))

#envoiStats(s_smtp,from_addr,to_addrs,sujet,dacgl_stats)

infos = collecte()
