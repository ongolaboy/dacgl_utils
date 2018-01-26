# -*-coding:utf-8 -*-

from datetime import date
from django.db import models


# Create your models here.
class Personnel(models.Model):
    """Infos génériques sur le personnel du bureau."""

    nom = models.CharField(max_length=200,primary_key=True)

    def __str__(self):
        return self.nom


class Equipement(models.Model):
    marque = models.CharField(max_length=200,default="HP")
    modele = models.CharField(max_length=200,blank=True)
    num_serie = models.CharField("Numéro de série",
            max_length=200,unique=True,default='x')
    date_acquisition = models.DateField("Date d'acquisition")

    def __str__(self):
        return "{0} {1}".format(self.marque,self.modele)


class Imprimante(Equipement):
    """Informations sur les imprimantes du bureau"""

    CATEGORIE_IMPRIMANTE = (
            ("encre","Jet d'encre"),
            ("laser","Laser"),
            ("multifonction","Multifonction"),
            )

    emplacement = models.CharField(max_length=200,default='Bureau')
    fqdn = models.CharField("Nom DNS",max_length=200,default='imprimante')
    categorie = \
            models.CharField(\
            "Type d'imprimante",
            max_length=20,
            choices=CATEGORIE_IMPRIMANTE,
            default='encre',
            )

    def __str__(self):
        return "{0} ({1})".format(self.modele,self.emplacement)


class Consommable(Equipement):
    """Informations sur les consommables du bureau"""

    NOM_COULEUR = (
            ("noir","noir"),
            ("jaune","jaune"),
            ("cyan","cyan"),
            ("magenta","magenta"),
            ("mixte","mixte"),
            )

    couleur = models.CharField(max_length=20,choices=NOM_COULEUR,
            default='noir')
    date_expiration = models.DateField(
            default=date.today().replace(year=date.today().year+1),
    help_text="ou date de fin de garantie"
    )
    disponible = models.BooleanField(default=True)
    date_retrait = models.DateField("date du retrait",\
            null=True,blank=True)
    imprimante_compatible = models.ManyToManyField(Imprimante,blank=True)
    commentaire = models.TextField(blank=True)

    class Meta:
        ordering = ['-disponible','disponible','date_expiration']

    def __str__(self):
        return "{0} {1} ({2})".format(\
                self.modele,self.couleur,self.num_serie)


class RetraitConsommable(models.Model):
    demandeur = models.ForeignKey(Personnel)
    date_retrait = models.DateField("date du retrait",auto_now_add=True)
    code_consommable = models.OneToOneField(Consommable)
    imprimante_utilisee = models.ForeignKey(Imprimante)

    class Meta:
        verbose_name = verbose_name_plural = "Retrait des consommables"

    def __str__(self):
        annee_date_retrait = self.date_retrait.year
        mois_date_retrait = self.date_retrait.month
        jour_date_retrait = self.date_retrait.day
        return "{0} retire pour {1} le {2}/{3}/{4}".format(\
                self.code_consommable,
                self.demandeur,jour_date_retrait,mois_date_retrait,
                annee_date_retrait)

    def save(self,*args,**kwargs):
        """
        Lorsqu'on effectue un retrait, il faut absolument changer
        le statut du consommable afin qu'il soit vu comme
        non disponible
        """
        c = Consommable.objects.get(pk=self.code_consommable)
        c.disponible = False
        c.date_retrait = date.today()
        c.save()
        super(RetraitConsommable,self).save(*args,**kwargs)
