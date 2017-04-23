#-*- coding: utf-8 -*-
from datetime import datetime
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

class PieceId(models.Model):

    PIECE = (
            ('passeport','passeport'),
            ('cni','CNI'),
            ('recepisse','recepisse'),
            ('autre','autre carte'),
            )
    typePiece = models.CharField(max_length=15,choices=PIECE)
    date_expiration = models.DateField(blank=True,null=True)
    code = models.CharField(\
            "Numéro ou code de la pièce",max_length=60,default=0,\
            help_text="Pour autre,laisser '0'")

    def __unicode__(self):
        return 'Piece: %s | id: %s ' % (self.typePiece, self.code)

#un usager peut se rendre dans un ou plusieurs services
#un service peut recvoir un ou plusieurs usagers
class Usager(models.Model):
    SEXE = (('H','homme'),('F','femme'),)
    nom_usgr = models.CharField("Nom & Prenom", max_length=50)
    sexe = models.CharField(max_length=5,choices=SEXE,default='H')
    piece = models.ForeignKey(PieceId)
    email = models.EmailField(blank=True)
    telephone = models.IntegerField(blank=True,null=True)

    services = models.ManyToManyField(Service, through='Visite')

    def __unicode__(self): return self.nom_usgr

#une visite correspond a un usager qui vient et part a une date  et heure precise 
# une visite peut correspondre a un ou plusieurs services
#on devrait pourvoir faire les statistiques des visites par usager et par service
class Visite(models.Model):
    #TODO changer heur_arr par dateArrivee
    heur_arr = models.DateTimeField('Heure Arrivée',\
            default=datetime.now())
    heur_deprt = models.DateTimeField('Heure Depart',blank=True,null=True)
#            default=datetime.today().replace(year=datetime.today().hour+1)
    type_visit = models.TextField('Objet de la Visite', default='AUF'
            )
    service = models.ForeignKey(Service)
    usager = models.ForeignKey(Usager)
    
       
    def __unicode__(self):
        return "{0} s'est rendu au {1}".format(self.usager, self.service)     

#formulaire pour enregistrement d'une visite
class ContactForm(ModelForm):
    class Meta:
        model = Usager
        fields = '__all__'       

