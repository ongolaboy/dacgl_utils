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


"""
Collecter des données issues de ces visites
à l'échelle du mois.

Récolter des informations suite à la saisie de toutes ces infos
et les envoyer par courriel
"""

BASE_DIR = '/home/devpy3/dacgl'
sys.path.append(BASE_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "dacgl.settings"


django.setup()

from dacgl.settings import TIME_ZONE
from id2.models import Visite,Usager,Service

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
    if t_actuel.month == 1:
        month0=12
        year0 = t_actuel.year - 1
        day0 = 31
        tz=timezone.get_current_timezone()
        t_fin_mois_prec = datetime(year=year0, month=month0,day=day0,tzinfo=tz)
    else :
        month0 = t_actuel.month - 1
        #pour la fin , on cherche d'abord le dernier jour
        #ensuite on va à 23h
        t_fin_mois_prec = (t_actuel - timedelta(days=t_actuel.day)).\
                replace(hour=23)

    t_debut_mois_prec = t_actuel.replace(month=month0,
            year = year0,
            day = 1,
            hour = 0,
            minute = 0,
            )
    visit_mois_prec = Visite.objects.filter(date_arrivee__range=\
            (t_debut_mois_prec,t_fin_mois_prec))

    services = []
    for s in Service.objects.all():
        services.append(s.nom_serv)

    visit = {}
    for v in services:
        visit[v] = visit_mois_prec.filter(service__nom_serv=v).count()
        visit[v+'2'] = visit_mois_prec.filter(service__nom_serv=v).\
                values('usager').distinct().count()
    visit['TOTAL'] = visit_mois_prec.count()
    visit['TOTAL2'] = visit_mois_prec.values('usager').distinct().count()

    usagers_enreg = {}
    usagers_enreg['TOTAL'] = Usager.objects.count()
    usagers_enreg['Courant'] = Usager.objects.filter(\
            visite__date_arrivee__range=\
            (t_debut_mois_prec,t_fin_mois_prec)).count()

    #Usager.objects.annotate(nbr_visit=Count('visite'))
    #Usager.objects.filter(visite__date_arrivee__range=(debut,maintenant))

    dacgl_stats = [usagers_enreg,visit,t_debut_mois_prec]

    return dacgl_stats

# section envoi courriel

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
            return 'stats fréquentations mensuelles DACGL envoyées'
    except Exception:
        return "Oups :-("



infos = collecte()

#pense bête
#len(infos) = 2 . infos[0]['TOTAL']; infos[1]['CNF']



infoUtiles0 = \
"""
Nombre d'usagers au total: %s
""" % infos[0]['TOTAL']

infoUtiles=''
for i in infos[1].keys():
    if i == 'TOTAL':
        visit_total = infos[1][i]
    else:
        if i =='TOTAL2':
            visit_total_dist = infos[1][i]
        else:
            infoUtiles += \
            """
            <tr>
             <td>%s </td><td>%s </td>
            </tr>
            """ % (i,infos[1][i])

#on positionne le total à la fin
infoUtiles +=\
"""
<tr>
 <td>%s </td><td>%s </td>
</tr>
<tr>
 <td>%s </td><td>%s </td>
</tr>
""" % ('TOTAL',visit_total,'TOTAL2',visit_total_dist)

pageWeb=\
        """
        <p>Details a l'adresse <a href="http://utils3.cm.auf.org/">
                    http://utils3.cm.auf.org/</a>.</p>
"""

ossature =\
"""
<html>

  <head>
   <title> Stats sur la frequentation - DACGL</title>
  </head>

  <body>
    <p>%s</p> <br/>
    <p>Les colonnes avec '2' correspondent aux visites distinctes par
    personnes</p> <br/>
    <p>Nous nous excusons pour  le formatage actuel de ces informations</p><br
    />
    <table border=1>
      <tr>
        <th>Service ou bureau</th><th>Nombre visites</th>
      </tr>
      %s
    </table>
    %s
  </body>

</html>
""" % (infoUtiles0,infoUtiles,pageWeb)


# section expédition du courriel

s_smtp = "smtp.cm.auf.org"
from_addr = u'technique@cm.auf.org'
to_addrs = 'diffusion-bureau@cm.auf.org'
sujet = 'Informations sur les visites a la DACGL: Mois de %s' % \
        infos[2].strftime('%B') #TODO t_debut_ pas encore défini
msg_utils = ossature

envoiStats(s_smtp,from_addr,to_addrs,sujet,TIME_ZONE,msg_utils)
