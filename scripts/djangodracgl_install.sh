#!/bin/bash


# Initialisation
ENVPYTHON='lab/tp80'

mkdir -p $HOME/$ENVPYTHONlab

#Initialisation environnement python
virtualenv $HOME/$ENVPYTHON/


# On fixe le pré-requis
cat > $HOME/$ENVPYTHON/requirements.txt << __EOF__
django==1.7.11
pillow
__EOF__

source $HOME/$ENVPYTHON/bin/activate

pip install -r $HOME/$ENVPYTHON/requirements.txt

cd $HOME/$ENVPYTHON/

#on récupère le projet
git clone https://github.com/ongolaboy/dacgl_utils

cd $HOME/$ENVPYTHON/dacgl_utils

#python manage.py runserver 9008

#on sort de l'environnement
deactivate
