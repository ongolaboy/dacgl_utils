from django.contrib import admin

# Register your models here.
from .models import Societe, Commande, Piece,Salle,Implantation
from .models import Devise, Marque, Produit, Categorie

class SocieteAdmin(admin.ModelAdmin):
    list_display = ('nom','id_CODA')

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('description','section','numero',
    'livree_par','notes',
    )
    list_filter = ['section','livree_par',]
    search_fields = ['numero','description']

class PieceAdmin(admin.ModelAdmin):
#    date_hierarchy = 'date_acquisition'
    list_display = ('intitule',
            'date_acquisition',
            'code_inventaire','commande_coda',
            'usage',
            'modele',)
    list_filter = ['date_acquisition','usage',
            'categorie', 'emplacement__site',
            'emplacement','sortie_inventaire']
    search_fields = ['intitule',]

class PieceInline(admin.StackedInline):
    model = Piece


admin.site.register(Societe,SocieteAdmin)
admin.site.register(Implantation)
admin.site.register(Salle)
admin.site.register(Commande,CommandeAdmin)
admin.site.register(Piece,PieceAdmin)
admin.site.register(Devise)
admin.site.register(Marque)
admin.site.register(Produit)
admin.site.register(Categorie)
