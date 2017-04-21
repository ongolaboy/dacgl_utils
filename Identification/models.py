#-*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from django.db import models

# Create your models here.
#modele pour la connexion des utilisateurs deja enregistrés dans la partie administration
class Profil(models.Model):
    user = models.OneToOneField(User)  # La liaison OneToOne vers le modèle User
    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Service(models.Model):
    nom_serv = models.CharField("Service", max_length=30)

    def __unicode__(self): return self.nom_serv

# unemployé existe dans un service uniquement
class Employe(models.Model):
    nom_emplye = models.CharField("Nom & Prenom", max_length=30)
    fonction = models.CharField(max_length=30)
    service = models.ForeignKey(Service)

    def __unicode__(self): return self.nom_emplye

#un usager peut se rendre dans un ou plusieurs services
#un service peut recvoir un ou plusieurs usagers
class Usager(models.Model):
    nom_usgr = models.CharField("Nom & Prenom", max_length=50)
    CNI = models.IntegerField()
    email = models.EmailField()
    telephone = models.IntegerField()

    services = models.ManyToManyField(Service, through='Visite')

    def __unicode__(self): return self.nom_usgr

#une visite correspond a un usager qui vient et part a une date  et heure precise 
# une visite peut correspondre a un ou plusieurs services
#on devrait pourvoir faire les statistiques des visites par usager et par service
class Visite(models.Model):
    date_jour = models.DateField('Date du Jour', auto_now=True)
    heur_arr = models.TimeField('Heure Arrivée')
    heur_deprt = models.DateTimeField('Heure Depart')
    type_visit = models.CharField('Objet de la Visite', max_length=20)
    service = models.ForeignKey(Service)
    usager = models.ForeignKey(Usager)
    nbre = models.IntegerField(default=0)
    
       
    def __unicode__(self):
        return "{0} s'est rendu au {1}".format(self.usager, self.service)     

#formulaire pour enregistrement d'une visite
class ContactForm(ModelForm):
    class Meta:
        model = Usager
        fields = '__all__'       

