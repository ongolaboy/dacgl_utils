#-*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils import timezone

class Service(models.Model):
    nom_serv = models.CharField("Service", max_length=30)

    def __unicode__(self): return self.nom_serv


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
            help_text="Pour autre,laisser '0'",
            unique=True)

    def __unicode__(self):
        return 'Piece: %s | id: %s ' % (self.typePiece, self.code)

#un usager peut se rendre dans un ou plusieurs services
#un service peut recvoir un ou plusieurs usagers
class Usager(models.Model):
    """
    Il s'agit ici de toute personne se présentant à la guérite
    indiféremment du fait qu'il soit abonné ou pas à un service
    de la maison
    """

    SEXE = (('H','homme'),('F','femme'),)
    nom = models.CharField("Nom", max_length=50)
    prenom = models.CharField("Prenoms", max_length=50,default='')
    sexe = models.CharField(max_length=5,choices=SEXE,default='H')
    piece = models.ForeignKey(PieceId)
    email = models.EmailField(blank=True)
    telephone = models.IntegerField(blank=True,null=True)

    services = models.ManyToManyField(Service, through='Visite')

    def __unicode__(self): return self.nom

    class Meta:
        unique_together = (('nom','prenom'),) #absolument

#une visite correspond a un usager qui vient et part a une date  et heure precise 
# une visite peut correspondre a un ou plusieurs services
#on devrait pourvoir faire les statistiques des visites par usager et par service
class Visite(models.Model):
    date_arrivee = models.DateTimeField('Heure Arrivée',\
            default=timezone.now(),
                auto_now_add=True)
    date_deprt = models.DateTimeField('Heure Depart',blank=True,null=True)
#            default=datetime.today().replace(year=datetime.today().hour+1)
    type_visit = models.TextField('Objet de la Visite', default='AUF'
            )
    service = models.ForeignKey(Service)
    usager = models.ForeignKey(Usager)
    
       
    def __unicode__(self):
        return "{0} s'est rendu au {1}".format(self.usager, self.service)

class Abonne(models.Model):
    usager = models.ForeignKey(Usager)
    service = models.ForeignKey(Service)
    matricule = models.CharField(\
            u"Identifiant de l'abonné",max_length=60,default=0,\
            help_text=u"Code généré suivant les règles du service",
            unique=True)
    photo = models.ImageField(upload_to="id2/photos/%Y/%m/%d",
            null=True,blank=True,
            )
    inscription = models.DateTimeField(default=timezone.now(),
            auto_now_add=True)
    expiration = models.DateField(blank=True, null=True)
    derniere_modif = models.DateTimeField(default=timezone.now(),
            auto_now=True)

    class Meta:
        unique_together = (('usager','service'),) #absolument

    def __unicode__(self):
        return "Matricule: %s |Date Inscription: %s" % \
                (self.matricule,self.inscription)
