import csv
import random

from datetime import datetime,date
from io import TextIOWrapper

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect,\
        HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Piece,Implantation,Marque,Salle,Produit,Commande,\
        Devise,Categorie
from .forms import inventaireLegacyForm, implantationForm

def code_aleatoire(pas=5):
    """Un code inventaire temporaire

    Au cas où il n'existe pas de code d'inventaire,cette fonction
    permet d'attribuer un code qui pourra éventuellement être changé
    par la suite
    """

    alea = ('abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQUVW')
    nbr_alea = 'X '
    trouve = False
    while trouve == False:

        while pas != 0:
            nbr_alea += random.choice(alea)
            pas -=  1

        try:
            Piece.objects.get(code_inventaire=nbr_alea)
        except:
            trouve = True
    return nbr_alea


def index(request):

    contexte = {}
    pT = Piece.objects.all()
    p = pT.order_by('-date_acquisition')[:40]
    implantations = Implantation.objects.all()
    # on fixe arbitrairement le périmètre «global» à 30
    contexte = {'piece': p, 'pT':pT,'implantations': implantations,
            'perimetre0': 30,}


    if request.method == "GET":
        form = implantationForm(request.GET)
        if form.is_valid():
            site_X = form.cleaned_data['implantationX']
            contexte['perimetre'] = site_X.id
            implantationX = Implantation.objects.get(pk=site_X.id)
            pX_T = Piece.objects.\
                filter(emplacement__site__id=site_X.id)
            if len(pX_T) == 0:
                message = 'Aucune information pour %s' % site_X.nom
                contexte['message'] = message
            else :
                pX = pX_T.order_by('-date_acquisition')[:40]
                contexte['pX_T'] = pX_T
                contexte['pX'] = pX
            contexte['implantationX'] = implantationX

    form = implantationForm()
    contexte['form']  = form

    return render(request,'inventaire2/index2.html', contexte)

def siteInfos(request,site_id):

    infos = Implantation.objects.get(pk=site_id)
    contexte = {'infos': infos }
    return render(request,'inventaire2/site.html', contexte)

def extraction(request,perimetre):

    fuseau = timezone.get_current_timezone()
    moment = datetime.now(fuseau)

    format_res = 'inventaire_'+ str(moment.year) +\
            str(moment.month) + str(moment.day) +\
            str(moment.hour) + str(moment.second)

    info_MIME = "attachment;filename=" + format_res

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = info_MIME + '.csv'
    
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

    if perimetre == '30':
        piece_a_extraire = Piece.objects.all()
    else:
        piece_a_extraire = \
                Piece.objects.filter(emplacement__site__id=perimetre)

    for piece in piece_a_extraire:
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

def extractionOld(request):
    return HttpResponsePermanentRedirect('/inventaire2/extraction/csv/30')

@login_required(login_url='/login/')
def importation(request):

    form = inventaireLegacyForm()
    contexte = {'form': form,}
    return render(request,'inventaire2/importation-csv.html',
            contexte)

def importationProcess(request):
    """Importation des données des autres sites

    Certaines informations seront fournies par défaut.
    Commande CODA: COM-INF 1
    valeur : 0 XAF
    """

    contexte = {}
    if request.method == 'POST':
        form = inventaireLegacyForm(request.POST,request.FILES)
        if form.is_valid():
            f = request.FILES['fichier']
            if f.content_type == 'text/csv':
            # les fichiers ici sont TOUS binaires d'où l'usage de io
            #pour csv qui a besoin de fichiers textes
                f = TextIOWrapper(f.file, encoding='UTF-8')
                csvfile = csv.reader(f,delimiter=',')

                premiere_ligne = True
                ligne = 0
                nbr_lignes_OK = 0
                lignes_Not_OK = []

                for colonne in csvfile:
                    ligne +=1
                    if premiere_ligne :
                        premiere_ligne = False
                        continue

                    #Implantation
                    try:
                        implantation0 = Implantation.objects.get(\
                                nom__icontains=colonne[0])
                    except Implantation.DoesNotExist:
                        implantation0 = Implantation(nom=colonne[0])
                        implantation0.save()

                    #Salle
                    try:
                        salle0 = implantation0.salle_set.get(\
                                nom__icontains=colonne[1])
                    except Salle.DoesNotExist:
                        salle0 = Salle(nom=colonne[1],site=implantation0)
                        salle0.save()

                    #Marque
                    if colonne[14] == '':
                        marque0,marque0_cree = Marque.objects.\
                                get_or_create(nom='INCONNU')
                    else:
                        try:
                            marque0 = Marque.objects.get(nom__icontains=\
                                    colonne[14])
                        except Marque.MultipleObjectsReturned:
                            marque0 = Marque.objects.filter(\
                                    nom__icontains=colonne[14]).first()
                        except Marque.DoesNotExist:
                            marque0 = Marque(nom=colonne[14])
                            marque0.save()

                    #Produit
                    if colonne[15] == '':
                        produit0,produit0_cree = marque0.produit_set.\
                                get_or_create(modele='INCONNU')
                    else:
                        try:
                            produit0 = marque0.produit_set.get(\
                                    modele__icontains=colonne[15])
                        except Produit.MultipleObjectsReturned :
                            produit0 = marque0.produit_set.filter(\
                                    modele__icontains=colonne[15]).first()
                        except Produit.DoesNotExist:
                            produit0 = Produit(modele=colonne[15],
                                    constructeur=marque0)
                            produit0.save()

                    try:
                        devise0 = Devise.objects.get(\
                                identifiant=colonne[5])
                    except Devise.DoesNotExist:
                        devise0 = Devise.objects.get(identifiant='XAF')

                    descr0 = ''
                    comm0 = ''
                    p_achat0 = 0

                    if colonne[4] != '':
                        p_achat0 = int(colonne[4])
                    usage0 = 'personnel'
                    if colonne[8] != '':
                        for u in Piece.USAGE:
                            if colonne[8] == u[0]:
                                usage0 = colonne[8]
                                break
                    if colonne[10] == '':
                        code_inventaire0 = code_aleatoire()
                    else:
                        code_inventaire0 = colonne[10]
                    if colonne[16] != '':
                        descr0 = colonne[16]
                    if colonne[17] != '':
                        comm0 = colonne[17]

                    piece = Piece(intitule = colonne[3],
                            prix_achat = p_achat0,
                        devise = devise0,
                        usage = usage0,
                        date_acquisition = date.today(),
                        code_inventaire = code_inventaire0,
                        description = descr0,
                        commentaire = comm0,
                        emplacement = salle0,
                        #on rappelle qu'on se sert par défaut de
                        #la COM-INF 1
                        #Pour la démo, j'ai fixé à 89 
                        #TODO à améliorer
                        commande_coda = \
                                Commande.objects.get(numero=89),
                        modele = produit0,
                        categorie = Categorie.objects.get(\
                                nom=colonne[2]),
                        )
                    piece.save()
                    nbr_lignes_OK += 1

                    #else:
                        # cette pièce a déjà été inventoriée
                    #    lignes_Not_OK.append(ligne)

                contexte = {'lignes_Not_OK': lignes_Not_OK,
                        'nbr_lignes_OK': nbr_lignes_OK,
                        'total_lignes': ligne,
                        'f': f,
                        }

                return render(request,
                'inventaire2/importation-csv-report.html',
                contexte, status=302)

            else :
                form = inventaireLegacyForm()
                contexte = {'message': "votre fichier n'est pas au \
                        format CSV",
                        'form': form,
                        'f':f,
                        'F':dir(f),
                        }
                return render(request, 'inventaire2/importation-csv.html',
                        contexte,status=302)
        else:
            form = inventaireLegacyForm()
            contexte['message'] = "le formulaire n'est pas valide"

            return HttpResponseRedirect(reverse('importation',
                kwargs = contexte))
            #return render(request,
            #'inventaire2/importation-csv.html',
            #contexte,
            #)
    else:
        form = inventaireLegacyForm()
        contexte = {'message': 'Veuillez recommencer svp',
                'form': form }
        return  render(request,'inventaire2/importation-csv.html',
                contexte)
