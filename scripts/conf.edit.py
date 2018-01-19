#renommer le fichier en conf.py pour l'exécution
"""
Variables dépendant de chaque site

BASE_DIR: repertoire contenant le projet django

SITE : nom du site local: CNF de ..., Antenne de ..

ACCUEIL_URL  : adresse à laquelle on peut voir le détail des visites

ACCUEIL : Message d'accueil envoyé avec les stats

s_smtp : nom du serveur smtp pour l'expédition

from_addr : adresse électronique de l'expéditeur

to_addrs : adresse destinataire du message

sujet : sujet du courriel qui sera envoyé
"""

BASE_DIR = ''
SITE = ''
ACCUEIL_URL = ""
ACCUEIL = "Page d'accueil {0}".format(ACCUEIL_URL)

#Messagerie
s_smtp = ""
from_addr = ''
to_addrs = ''
