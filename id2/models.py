#-*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Societe(models.Model):
    """
    Organisme travaillant avec l'AUF.

    L'AUF reçoit régulièrement des employés d'autres structures.
    Il est souhaitable de classer ces personnes suivant leur boîte.
    """

    nom = models.CharField("Nom structure", max_length=30)
    adresse = models.TextField("Adresse physique")
    description = models.TextField("Description sommaire")
    email = models.EmailField(blank=True)
    telephone = models.IntegerField(blank=True,null=True)
    site_web = models.URLField(blank=True)

    def __str__(self): return self.nom

@python_2_unicode_compatible
class Service(models.Model):
    nom_serv = models.CharField("Service", max_length=30)

    def __str__(self): return self.nom_serv

@python_2_unicode_compatible
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
            help_text="Pour autre,laisser '0'", blank=True,
            )

    def __str__(self):
        return 'Piece: %s | id: %s ' % (self.typePiece, self.code)

#un usager peut se rendre dans un ou plusieurs services
#un service peut recevoir un ou plusieurs usagers
@python_2_unicode_compatible
class Usager(models.Model):
    """
    Personne qui se présente à la guérite.

    Il s'agit ici de toute personne se présentant à la guérite
    indiféremment du fait qu'il soit abonné ou pas à un service
    de la maison
    """

    SEXE = (('H','homme'),('F','femme'),)
    nom = models.CharField("Nom", max_length=50)
    prenom = models.CharField("Prenoms", max_length=50,default='')
    sexe = models.CharField(max_length=5,choices=SEXE,default='H')
    piece = models.ForeignKey(PieceId,on_delete=models.CASCADE,
            blank=True)
    email = models.EmailField(blank=True)
    telephone = models.IntegerField(blank=True,null=True)
    en_dessous = models.BooleanField(help_text="Moins de 35 ans?",
            default=True)
    d_inscription = models.DateTimeField('Date inscription',\
            default=timezone.now,null=True)

    services = models.ManyToManyField(Service, through='Visite')

    def __str__(self): return self.nom

    class Meta:
        unique_together = (('nom','prenom'),) #absolument

@python_2_unicode_compatible
class Employe(models.Model):
    """
    Personne appartenant à une Société.

    Catégorie de personnes se présentant dans nos services de la part
    d'une structure et pour des besoins comme: dépôt de courrier,
    maintenance de clim, maintenance groupe,...
    """

    SEXE = (('H','homme'),('F','femme'),)

    nom = models.CharField("Nom", max_length=50)
    prenom = models.CharField("Prenoms", max_length=50,default='')
    sexe = models.CharField(max_length=5,choices=SEXE,default='H')
    piece = models.ForeignKey(PieceId,on_delete=models.CASCADE)
    structure = models.ForeignKey(Societe,on_delete=models.CASCADE)
    telephone = models.IntegerField(blank=True,null=True)
    email = models.EmailField(blank=True)

    def __str__(self): return self.nom

#une visite correspond a un usager qui vient et part a une date  et heure precise 
# une visite peut correspondre a un ou plusieurs services
#on devrait pourvoir faire les statistiques des visites par usager et par service
@python_2_unicode_compatible
class Visite(models.Model):
    date_arrivee = models.DateTimeField('Heure Arrivée',\
            default=timezone.now)
    date_deprt = models.DateTimeField('Heure Depart',blank=True,null=True)
#            default=datetime.today().replace(year=datetime.today().hour+1)
    type_visit = models.TextField('Objet de la Visite', default='AUF'
            )
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    usager = models.ForeignKey(Usager,on_delete=models.CASCADE)
    
       
    def __str__(self):
        return "{0} s'est rendu au {1}".format(self.usager, self.service)

@python_2_unicode_compatible
class VisiteProf(models.Model):
    date_arrivee = models.DateTimeField('Heure Arrivée',\
            default=timezone.now)
    date_deprt = models.DateTimeField('Heure Depart',blank=True,null=True)
    type_visit = models.TextField('Objet de la Visite', default='Courrier'
            )
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    employe = models.ForeignKey(Employe,on_delete=models.CASCADE)

    def __str__(self):
        return "{0} s'est rendu au {1}".format(self.employe, self.service)

#TODO créer une classe abstraite pour les abonnés
# et disposer d'une classe d'abonné CNF et une autre fablab
@python_2_unicode_compatible
class Abonne(models.Model):
    usager = models.ForeignKey(Usager,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    matricule = models.CharField(\
            u"Identifiant de l'abonné",max_length=60,default=0,\
            help_text=u"Code généré suivant les règles du service",
            unique=True)
    photo = models.ImageField(upload_to="id2/photos/%Y/%m/%d",
            null=True,blank=True,
            )
    inscription = models.DateTimeField(default=timezone.now)
    expiration = models.DateField(blank=True, null=True)
    derniere_modif = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('usager','service'),) #absolument

    def __str__(self):
        return "Matricule: %s |Date Inscription: %s" % \
                (self.matricule,self.inscription)
