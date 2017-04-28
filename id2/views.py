#-*- coding: utf-8 -*-

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render

from id2.forms import InscriptionForm,VisiteForm,RechercheForm
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
    u = Usager.objects.latest('pk')
    message = "%s %s" % (u.nom,u.prenom)
    contexte = {'message': message,'form':form}

    return render(request,'id2/inscription.html',contexte)

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

def recherche(request):
    form = RechercheForm()
    return render(request,'id2/recherche.html',{'form':form})

def rechercheTraitement(request):
    contexte = {}
    if request.method == 'GET':
        form = RechercheForm(request.GET)
        if form.is_valid():
            terme = form.cleaned_data['terme']
            resultat = Usager.objects.filter(nom__contains=terme)
            contexte = {'resultat': resultat,
                    'terme': terme,
                    }

            return render(request,
                    'id2/resultat.html',
                   contexte,
                    status=302
                    )
        else:
            message = 'Veuillez vérifier votre saisie'
            contexte = {'error_message':message,
                    'form':form}
            return render(request,'id2/recherche.html',contexte)
    else:
        form = RechercheForm()
        return HttpResponseRedirect('/ident/recherche/')

@login_required(login_url='/ident/')
def visite(request,usager_id):
    """
    A travers cette vue on va consigner l'heure d'arrivée
    d'un usager
    """

    try :
        u = Usager.objects.get(pk=usager_id)
        data = {'nom': u.nom, 'prenom': u.prenom}
        #on lie les données au formulaire
        form = VisiteForm(data)

        contexte = {
                'form': form,
                }
        return render(request,'id2/visite.html',contexte)
    except Usager.DoesNotExist:
        message = 'Veuillez enregistrer cet usager au préalable'
        form = InscriptionForm()
        contexte = {'form': form,
                'error_message': message,
                }
        return render(request,'id2/inscription.html',
                contexte,status=302)





def visiteTraitement(request):
    pass

def sortie(request):
    logout(request)
    return HttpResponseRedirect('/ident/')
