#!/bin/bash


# Initialisation
ENVPYTHON='lab/tp80'
PORT_PROJET=9008


source $HOME/$ENVPYTHON/bin/activate

cd $HOME/$ENVPYTHON/dacgl_utils

#on démarre le serveur web (de développement)
python manage.py runserver $PORT_PROJET
