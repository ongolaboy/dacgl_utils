# -*- coding:utf-8 -*-

"""Fonctions utiles
"""

from datetime import datetime,timedelta
from django.utils import timezone

from id2.models import Visite,Usager,Service

def periodes(annee,mois=''):
    """
    1er et dernier jour d'une période

    m1 est le premier jour du mois
    m2 est le dernier jour du mois
    """

    tz = timezone.get_current_timezone()
    t_actuel = datetime.now(tz)
    periode = {}
    if mois in range(1,13):
        #le jour 1 dès 7h; le jour 2 à 21h
        m1 = datetime(annee,mois,1,7,tzinfo=tz)
        if mois == 12:
            #quoique ... on ferme bien avant le 31 !
            m2 = m1.replace(day=31)
        else:
            m2 = m1.replace(month = m1.month+1) - timedelta(days=1)
        m2 = m2.replace(hour=21)
        periode[mois] = (m1,m2)

    else :
        #on veut les périodes sur 12 mois
        for m in range(1,13):
            m1 = datetime(annee,month=m,day=1,tzinfo=tz)
            if m == 12:
                m2 = m1.replace(day=31)
            else:
                m2 = m1.replace(month = m1.month+1) - timedelta(days=1)
            periode[m] = [m1,m2]

    return periode

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

    if mois in range(1,13):
        pass
    else:
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
