# -*- coding:utf-8 -*-

from django.contrib import admin
from bureautique.models import Personnel, Imprimante, Consommable
from bureautique.models import RetraitConsommable

class ConsommableAdmin(admin.ModelAdmin):
    list_display = ('__str__','couleur',
            'date_expiration','disponible','date_retrait')
    list_filter = ['disponible','date_expiration','modele']
    ordering = ['-disponible','couleur','date_expiration']

class RetraitConsommableAdmin(admin.ModelAdmin):
    list_display = ('date_retrait','demandeur','imprimante_utilisee',
            'code_consommable')
    list_filter = ['demandeur','imprimante_utilisee']
    ordering = ['-date_retrait']

admin.site.register(Personnel)
admin.site.register(Imprimante)
admin.site.register(Consommable,ConsommableAdmin)
admin.site.register(RetraitConsommable,RetraitConsommableAdmin)
