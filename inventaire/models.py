#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.

DEVISE = (
        ('XAF','Francs CFA'),
        ('USD','Dollars US'),
        ('EUR','Euros'),
        )

class Categorie(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Ville(models.Model):
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom

class Societe(models.Model):
    """
    Fournisseurs, prestataires, entreprises avec lesquelles
    on a déjà eu à effectuer des achats.
    """

    nom = models.CharField("Nom structure", max_length=30)
    adresse = models.TextField("Adresse physique")
    description = models.TextField("Description sommaire")
    email = models.EmailField(blank=True)
    telephone = models.IntegerField(blank=True,null=True)
    site_web = models.URLField(blank=True)
    code_CODA = models.CharField(max_length=20, blank=True)

    def __str__(self): return self.nom


class Commande(models.Model):
    """
    Informations relatives aux commandes issues
    de CODA
    """

    SECTION = (
            ('INF','COM-INF'),
            ('ARE','COM-ARE'),
            )

    description = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    valeur = models.PositiveIntegerField()
    section = models.CharField(max_length=10, choices=SECTION,
            default='INF')
    numero = models.PositiveIntegerField()
    devise = models.CharField(max_length=10, choices=DEVISE,
            default='EUR')
    notes = models.TextField()

    def __str__(self):
        return "%s %s | %s %s" % (self.section,self.numero,
                self.valeur, self.devise)


class Ensemble(models.Model):
    """
    Il peut s'agir d'une visio qui contient plusieurs éléments,
    d'un serveur avec ses disques durs,etc.
    """
    
    ETAT = (
            ('OK','Fonctionnel'),
            ('NO','En panne'),
            ('Reserve','Reserve'),
            ('OUT','Sortie'),
            )

    modele = models.CharField(max_length=200)
    description = models.TextField()
    prix_achat = models.PositiveIntegerField()
    devise = models.CharField(max_length=10, choices=DEVISE,
            default='EUR')
    etat = models.CharField(max_length=20, choices=ETAT,
            default='OK')
    commentaire = models.TextField()
    emplacement = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)

    def __str__(self):
        return ('%s %s %s') % (self.modele, self.prix_achat, self.devise)


class Piece(models.Model):
    """
    Identification de la plus petite unité:
    une caméra, un disque,.. ou d'une pièce unique ex:
    ordinateur portable
    """

    num_serie = models.CharField(max_length=200)
    modele = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    date_acquisition = models.DateField()
    code_inventaire = models.CharField(max_length=100)
    comm_coda = models.ForeignKey("Commande sur CODA",Commande,
            on_delete= models.CASCADE)
    ensemble = models.ForeignKey(Ensemble,
            on_delete= models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.num_serie,
                self.description,self.code_inventaire)
