#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.


class Devise(models.Model):
    identifiant = models.CharField(max_length=8,
            primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Implantation(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=30)
    site = models.ForeignKey(Implantation,
            on_delete = models.CASCADE)

    class Meta:
        unique_together = ('nom','site')
        ordering = ['site','nom']

    def __str__(self):
        return '%s:%s' % (self.site, self.nom)


class Marque(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Produit(models.Model):
    modele = models.CharField(max_length=100, blank=True)
    constructeur = models.ForeignKey(Marque,
            on_delete=models.CASCADE)

    class Meta:
        unique_together = ('modele','constructeur')
        ordering = ['constructeur','modele']

    def __str__(self):
        return "%s %s" % (self.constructeur, self.modele)


class Categorie(models.Model):
    nom = models.CharField(max_length=200,
            help_text=u"Mobilier,info,élec,...")

    class Meta:
        ordering = ['nom']

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

    class Meta:
        ordering = ['nom']

    def __str__(self): return self.nom


class Commande(models.Model):
    """
    Informations relatives aux commandes issues
    de CODA
    """

    SECTION = (
            ('INF','COM-INF'),
            ('ARE','COM-ARE'),
            ('AUTRE','Autre'),
            )

    description = models.CharField(max_length=200, blank=True)
    valeur = models.PositiveIntegerField(blank=True)
    section = models.CharField(max_length=10, choices=SECTION,
            default='INF',
            help_text=u"Utilisez 'Autre' si vous ne connaissez pas \
                    la commande")
    numero = models.PositiveIntegerField(help_text=u"Numéro \
            commande")
    devise = models.ForeignKey(Devise,
            on_delete=models.CASCADE)
    livree_par = models.ForeignKey(Societe,
            on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('section','numero')
        ordering = ['section','numero']

    def __str__(self):
        return "COM %s : %s | %s %s" % (self.section,self.numero,
                self.valeur, self.devise)


class Piece(models.Model):
    """
    Identification de la plus petite unité:
    une caméra, un disque,.. ou d'une pièce unique ex:
    ordinateur portable
    """

    USAGE = (
            ('personnel','Personnel'),
            ('infrastructure','Infrastructure'),
            ('usager','Usager'),
            ('projet','Projet'),
            )

    intitule = models.CharField(max_length=200, default="Piece")
    prix_achat = models.PositiveIntegerField(default=0)
    devise = models.ForeignKey(Devise,
            on_delete=models.CASCADE)
    num_serie = models.CharField(u"Numéro de série",max_length=200,
            blank=True)
    fonctionnel = models.BooleanField(help_text="Est-ce que ça marche?",
            default=True)
    usage = models.CharField(max_length=20, choices=USAGE,
            help_text="Personnel,usager ?",default='personnel')
    date_acquisition = models.DateField()
    code_inventaire = models.CharField(max_length=100, unique=True,
            help_text="ex CG1 I9012")
    description = models.CharField(max_length=200, blank=True)
    commentaire = models.TextField(blank=True)
    emplacement = models.ForeignKey(Salle,
            on_delete = models.CASCADE)
    commande_coda = models.ForeignKey(Commande,
            on_delete= models.CASCADE, blank=True)
    modele = models.ForeignKey(Produit,
            on_delete= models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    sortie_inventaire = models.BooleanField(default=False,
            help_text="Sortie d'inventaire ?")
    periode_amortissement = models.PositiveIntegerField(default=4,
            help_text=u"En nombre d'années")

    def __str__(self):
        return "%s %s %s" % (self.num_serie,
                self.description,self.code_inventaire)
