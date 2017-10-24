import csv

from django.http import HttpResponse
from django.shortcuts import render

from .models import Piece

# Create your views here.

def index(request):

    p = Piece.objects.all().order_by('-date_acquisition')[:40]
    contexte = {'piece': p}

    return render(request,'inventaire2/index.html',
            contexte)

def extraction(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;\
    filename='piece_sortie.csv'"
    
    total_piece = Piece.objects.all()
    writer = csv.writer(response)

    #TODO : laisser le choix à l'utilisateur
    entete = ['Site','Emplacement',
            "Catégorie",
            'Intitule',"Prix d'achat",
            "Devise",'Numéro de série',
            'Fonctionnel','Usage',
            "Date d'acquisition","Code d'inventaire",
            "Code document","Numéro CODA",
            "Valeur Commande CODA","Modèle",
            "Description",
            ]
    writer.writerow(entete)
            
    for piece in Piece.objects.all():
        code_document = 'COM-' + \
        piece.commande_coda.section

        ligne_fichier = [
                piece.emplacement.site.nom,
                piece.emplacement.nom,
                piece.categorie,
                piece.intitule,
                piece.prix_achat,
                piece.devise,
                piece.num_serie,
                piece.fonctionnel,
                piece.usage,
                piece.date_acquisition,
                piece.code_inventaire,
                code_document,
                piece.commande_coda.numero,
                piece.commande_coda.valeur,
                piece.modele,
                piece.description,
                ]
        writer.writerow(ligne_fichier)

    return response
