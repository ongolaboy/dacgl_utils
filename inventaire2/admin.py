from django.contrib import admin

# Register your models here.
from .models import Societe, Commande, Piece,Salle,Implantation
from .models import Devise, Marque, Produit, Categorie

class PieceAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_acquisition'
    list_display = ('intitule',
            'date_acquisition',
            'code_inventaire','commande_coda',
            'fonctionnel','usage',
            'modele','categorie')
    list_filter = ['date_acquisition','usage',
            'categorie', 'emplacement__site',
            'sortie_inventaire']

class PieceInline(admin.StackedInline):
    model = Piece

class CommandeAdmin(admin.ModelAdmin):
    inlines = [
            PieceInline,
            ]


admin.site.register(Societe)
admin.site.register(Implantation)
admin.site.register(Salle)
admin.site.register(Commande,CommandeAdmin)
admin.site.register(Piece,PieceAdmin)
admin.site.register(Devise)
admin.site.register(Marque)
admin.site.register(Produit)
admin.site.register(Categorie)
