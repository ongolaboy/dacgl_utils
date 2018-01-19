#!/bin/dash

# exploité par cron périodiquement
ANNEE=`date +%G`
MOIS=`date +%m`

/usr/bin/env python3 /chemin/vers/dossier/script/projet/visites-infos2.py $ANNEE $MOIS courriel
