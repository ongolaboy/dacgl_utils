#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from id2.forms import InscriptionForm
from id2.models import Usager,PieceId

def index(request):
    
    contexte = {}

    return render(request,'id2/index.html',contexte)

def entree(request):
    return render(request,'id2/entree.html')

def entreeVerification(request):
    
    if request.method == 'POST':
        usern = request.POST['identifiant']
        passwd = request.POST['password']
        user = authenticate(username=usern, password = passwd)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/ident/inscription/')
            else :
                # compte désactivé
                return HttpResponseForbidden('/ident/')

    return HttpResponseRedirect('/ident/login/')

def inscription(request):
    """
    Saisie des informations relatives au passage d'un NOUVEL usager
    """

    form = InscriptionForm()

    return render(request,'id2/inscription.html',{'form':form})

def inscriptionTraitement(request):

    contexte = {}
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['nom']
            p = form.cleaned_data['prenom']
            s = form.cleaned_data['sexe']
            piece = form.cleaned_data['typePiece']
            cod = form.cleaned_data['code']
            date_expiration = form.cleaned_data['date_expiration']
            em = form.cleaned_data['email']
            tel = form.cleaned_data['telephone']

            #on passe aux vérifications AVANT de vouloir save
            try :
                u = Usager.objects.get(nom=n,prenom=p)
            except Usager.DoesNotExist:
                try :
                    piece0 = PieceId.objects.get(code=cod)
                #on va d'abord enregistrer la pièce
                except PieceId.DoesNotExist :
                    piece0 =\
                    PieceId(typePiece=piece,
                            date_expiration=date_expiration,
                            code=cod,
                            )
                    piece0.save()
                u = Usager(nom=n,sexe=s,prenom=p,
                        piece=piece0,
                        email=em,
                        telephone=tel)
                u.save()
                contexte = {'message': 'Inscription effectuée'}

            #tout est ok, on revient sur un formulaire vierge
            return HttpResponseRedirect('/ident/inscription/')

        #si le formulaire a des points non valides
        else :
            contexte = {'message': 'Veuillez revérifier votre saisie',
                    'form': form,
                    }
            return render(request,
                    'id2/inscription.html',
                    contexte,status=303) #lire rfc2616

    #si la méthode n'est pas de type POST
    else :
        form = InscriptionForm()
        contexte['message'] = 'Veuillez recommencer svp'
        return render(request,'id2/inscription.html',contexte)

def sortie(request):
    logout(request)
    return HttpResponseRedirect('/ident/')
