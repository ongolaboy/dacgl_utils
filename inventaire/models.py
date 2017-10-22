#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class Devise(models.Model):
    identifiant = models.CharField(max_length=8,
            primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Marque(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    modele = models.CharField(max_length=100)
    constructeur = models.ForeignKey(Marque,
            on_delete=models.CASCADE)

    def __str__(self):
        return self.modele


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
    id_CODA = models.CharField(max_length=20, blank=True)

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
    devise = models.ForeignKey(Devise,
            on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return "%s %s | %s %s" % (self.section,self.numero,
                self.valeur, self.devise)


class Ensemble(models.Model):
    """
    Il peut s'agir d'une visio qui contient plusieurs éléments,
    d'un serveur avec ses disques durs,etc.
    """
    
    USAGE = (
            ('personnel','Personnel'),
            ('infrastructure','Infrastructure'),
            ('usager','Usager'),
            ('projet','Projet'),
            )


    modele = models.CharField(max_length=200)
    description = models.TextField()
    prix_achat = models.PositiveIntegerField()
    devise = models.ForeignKey(Devise,
            on_delete=models.CASCADE)
    fonctionnel = models.BooleanField(default=True)
    usage = models.CharField(max_length=20, choices=USAGE,
            default='personnel')
    commentaire = models.TextField()
    emplacement = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    reserve = models.BooleanField(default=False)
    sortie = models.BooleanField(help_text="Sortie de stock ?",
            default=False)

    def __str__(self):
        return '%s %s %s' % (self.modele, self.prix_achat, self.devise)


class Piece(models.Model):
    """
    Identification de la plus petite unité:
    une caméra, un disque,.. ou d'une pièce unique ex:
    ordinateur portable
    """

    num_serie = models.CharField(u"Numéro de série",max_length=200)
    description = models.CharField(max_length=200, blank=True)
    date_acquisition = models.DateField()
    code_inventaire = models.CharField(max_length=100)
    comm_coda = models.ForeignKey(Commande,
            on_delete= models.CASCADE)
    ensemble = models.ForeignKey(Ensemble,
            on_delete= models.CASCADE)
    modele = models.ForeignKey(Produit,
            on_delete= models.CASCADE)

    def __str__(self):
        return "%s %s %s" % (self.num_serie,
                self.description,self.code_inventaire)
