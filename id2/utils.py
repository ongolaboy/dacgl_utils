"""Fonctions utiles
"""

from datetime import datetime,timedelta
from django.utils import timezone

from id2.models import Visite,Usager,Service

def periodes(annee):
    """
    Liste contenant le 1er et dernier jour de chaque mois

    m1 est le premier jour du mois
    m2 est le dernier jour du mois
    """

    tz = timezone.get_current_timezone()
    t_actuel = datetime.now(tz)
    periode = {}

    for m in range(1,13):
        m1 = datetime(annee,month=m,day=1,tzinfo=tz)
        if m == 12:
            m2 = m1.replace(day=31)
        else:
            m2 = m1.replace(month = m1.month+1) - timedelta(days=1)
        periode[m] = [m1,m2]

    return periode

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
    p = periodes(annee) #TODO vérifier si ça marche


    services = []
    for s in Service.objects.all():
        services.append(s.nom_serv)

    #Visite.objects.filter(date_arrivee__range=(mois[5][0],mois[5][1]))
    v_Total =\
            Visite.objects.filter(date_arrivee__range=(p[1][0],p[12][1]))
    visit = {}
    usagers_enreg = {}
    for m in range(1,13):
        for v in services:
            v0 = v_Total.filter(service__nom_serv=v)
            visit[(v,m)] = []
            visit[(v,m)].append(v0.filter(\
                    date_arrivee__range=(p[m][0],p[m][1])))

        usagers_enreg[m] = Usager.objects.filter(\
                visite__date_arrivee__range=(p[m][0],p[m][1])
                )
        #visit[v] = (v0.count(),v0.values('usager').distinct().count())

    #Usager.objects.filter(visite__date_arrivee__range=(debut,maintenant))

    dacgl_stats = [usagers_enreg,visit]

    return dacgl_stats
