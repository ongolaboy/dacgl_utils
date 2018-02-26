# -*- coding:utf-8 -*-

from datetime import timedelta

from django.db import models
from django.utils import timezone

from id2.models import Usager,Service


class Evenement(models.Model):
    lieu = models.ForeignKey(Service, on_delete=models.PROTECT)
    intitule = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    debut = models.DateField()
    fin = models.DateField(blank=True,null=True)
    participant = models.ManyToManyField(Usager, through='Participation')
    ouvert = models.BooleanField(default=True)

    def duree(self):
        if self.fin is None:
            self.periode = (timedelta(days=1)).days
        else:
            self.periode = (self.fin - self.debut).days + 1
        return self.periode

    def __str__(self):
        return "{0} ({1})".format(self.intitule,self.lieu)


class Participation(models.Model):
    """Participation d'une personne à une manifestation."""

    usager = models.ForeignKey(Usager, on_delete=models.PROTECT)
    evenement = models.ForeignKey(Evenement, 
            on_delete=models.PROTECT)
    date_inscription = models.DateTimeField(default=timezone.now)
    commentaire = models.TextField(blank=True)

    class Meta:
        unique_together = (('usager','evenement'))

    def __str__(self):
        return "%s | %s" % (self.usager, self.evenement)
