import csv

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import Piece

# Create your views here.

def index(request):

    p = Piece.objects.all().order_by('-date_acquisition')[:40]
    contexte = {'piece': p}

    return render(request,'inventaire2/index.html',
            contexte)

def extraction(request):

    fuseau = timezone.get_current_timezone()
    moment = datetime.now(fuseau)

    format_res = 'inventaire_'+ str(moment.year) +\
            str(moment.month) + str(moment.day) +\
            str(moment.hour) + str(moment.second)

    info_MIME = "attachment;filename=" + format_res

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = info_MIME
    
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
            "Valeur Commande CODA","Marque","Modèle",
            "Description","Commentaire",
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
                piece.devise.identifiant,
                piece.num_serie,
                piece.fonctionnel,
                piece.usage,
                piece.date_acquisition,
                piece.code_inventaire,
                code_document,
                piece.commande_coda.numero,
                piece.commande_coda.valeur,
                piece.modele.constructeur.nom,
                piece.modele.modele,
                piece.description,
                piece.commentaire,
                ]
        writer.writerow(ligne_fichier)

    return response
