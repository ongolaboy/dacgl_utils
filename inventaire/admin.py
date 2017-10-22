from django.contrib import admin
from .models import Societe, Commande, Ensemble, Piece,Famille
from .models import Devise, Marque, Produit, Categorie,Ville

admin.site.register(Societe)
admin.site.register(Commande)
admin.site.register(Ensemble)
admin.site.register(Piece)
admin.site.register(Devise)
admin.site.register(Marque)
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Ville)
admin.site.register(Famille)
