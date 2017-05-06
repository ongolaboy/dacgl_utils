#-*- coding: utf-8 -*-

from datetime import date,datetime
from pytz import timezone

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from dacgl.settings import TIME_ZONE
from id2.forms import InscriptionForm,VisiteForm,RechercheForm
from id2.models import Usager,PieceId,Visite,Service


def index(request):
    
    contexte = {}
    u = Usager.objects.all().count()
    last_visit = Visite.objects.all().order_by('-date_arrivee')[:10]
    last_inscrit = Usager.objects.all().order_by('-id')[:10]
    #mois en cours
    m = date.today().month
    nbr_visit_current_month =\
            Visite.objects.filter(date_arrivee__month=m).count()

    contexte = {
            'usager':u,
            'derniereVisite': last_visit,
            'dernierInscrit': last_inscrit,
            'nVisitCeMois' : nbr_visit_current_month,
            }

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
                return HttpResponseRedirect('/ident/')
            else :
                # compte désactivé
                return HttpResponseForbidden('/ident/')

    return HttpResponseRedirect('/ident/login/')

def inscription(request):
    """
    Saisie des informations relatives au passage d'un NOUVEL usager
    """

    form = InscriptionForm()
    message = ''
    contexte = {}
    try:
        u = Usager.objects.latest('pk')
        message = "%s %s" % (u.nom,u.prenom)
        contexte = {'message': message,'form':form}
        return render(request,'id2/inscription.html',contexte)
    except Usager.DoesNotExist:
        contexte = {'message': message, 'form':form}
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
            resultat = Usager.objects.filter(nom__icontains=terme)
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
    A travers cette vue on va consigner automatiquement
    l'heure d'arrivée d'un usager.
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
    contexte = {}
    if request.method == 'POST':
        form = VisiteForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['nom']
            p = form.cleaned_data['prenom']
            s = form.cleaned_data['service']
            m = form.cleaned_data['motif']

            try:
                u = Usager.objects.get(nom=n,prenom=p)
                v = Visite(usager=u,
                        service=Service.objects.get(nom_serv=s),
                        type_visit=m)
                v.save()
                contexte = {'nom':u.nom,
                        'num':v.id,
                        }
                return render(request,'id2/visiteur-enregistre.html',\
                        contexte,status=302)

            except Usager.DoesNotExist:
                # faut trouver un usager qui existe dans la base
                return HttpResponseRedirect('/ident/recherche')
        else:
            contexte = {'message': 'Veuillez revérifier votre saisie',
                    'form': form,
                    }
            return render(request,
                    'id2/visite.html',
                    contexte,status=303)

    #la méthode n'était pas de type POST
    else:
        form = VisiteForm()
        return render(request,'id2/visite.html',{'form':form})

@login_required(login_url='/ident/login/')
def consignerDepart(request,visite_id):
    try :
        v = Visite.objects.get(pk=visite_id)
        u= Usager.objects.get(pk=v.usager_id)
        data = {'nom': u.nom,
                'prenom': u.prenom,
                'service': v.service,
                'motif': v.type_visit,
                'arrivee':v.date_arrivee,
                'visite_id':v.id,
                }
        return render(request,'id2/retour.html',data)

    except Visite.DoesNotExist:
        message = "Cette visite n'existe pas dans la base de données"
        return HttpResponseRedirect('/ident')

def consigneTraitement(request,visite_id):
    c = get_object_or_404(Visite, pk=visite_id)
    etat = request.POST['DepartAUF']

    if etat == 'Oui':
        if c.date_deprt != None:
            #quelque chose a déjà été enregistré et par conséquence
            # on n'ajoute plus rien
            #TODO songer à un meilleur contrôle
            return HttpResponseRedirect('/ident')
        else:
            c.date_deprt = datetime.now(timezone(TIME_ZONE))
            c.save(update_fields=['date_deprt'])
            return HttpResponseRedirect('/ident/')
    elif etat == 'Non':
        #rien à faire on revient à l'accueil
        return HttpResponseRedirect('/ident/')

def sortie(request):
    logout(request)
    return HttpResponseRedirect('/ident/')
