import csv

from datetime import datetime

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Piece
from .forms import inventaireLegacyForm

def csvToInventaire(f):
    with open(f, newline='') as csvfile:
        inventaire_orig = csv.reader(csvfile, delimiter=',')
        extraction_f = []
        for row in inventaire_orig:
            extraction_f.append(row)
        return extraction_f

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

def importation(request):

    form = inventaireLegacyForm()
    contexte = {'form': form,}
    return render(request,'inventaire2/importation-csv.html',
            contexte)

def importationProcess(request):
    contexte = {}
    if request.method == 'POST':
        form = inventaireLegacyForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['fichier']
            if f.content_type == 'text/csv':

                import_f = csvToInventaire(request.FILES['fichier'])
                for ligne in import_f:
                    try :
                        produit0 = \
                                Produit.objects.get(modele__icontains=\
                                ligne[15])
                    except Produit.MultipleObjectsReturned :
                        pass #TODO
                    except Produit.DoesNotExist:
                        #il faut vérifier que la marque soit présente
                        try :
                            marque0 = Marque.objects.get(nom__icontains=\
                                    ligne[14])
                        except Marque.DoesNotExist:
                            marque0 = Marque(nom=ligne[14])
                            marque0.save()

                        produit0.save()

                    p = Piece(intitule = ligne[3],
                            devise = ligne[5],
                            date_acquisition = ligne[9],
                            code_inventaire = ligne[10],
                            emplacement = ligne[1],
                            commande_coda = \
                                    Commande.objects.get(numero=1),
                            modele = produit0,
                            categorie = ligne[2],
                            )

                return HttpResponseRedirect('/inventaire2')
            else :
                form = inventaireLegacyForm()
                contexte = {'message': "votre fichier n'est pas au \
                        format CSV",
                        'form': form,
                        'f':f,
                        }
                return render(request, 'inventaire2/importation-csv.html',
                        contexte)
    else:
        form = inventaireLegacyForm()
        contexte = {'message': 'Veuillez recommencer svp',
                'form': form }
        return  render(request,'inventaire2/importation-csv.html',
                contexte)
