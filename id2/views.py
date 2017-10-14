#-*- coding: utf-8 -*-

from datetime import date,datetime,timedelta

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.utils import timezone

from id2.forms import InscriptionForm,VisiteForm,RechercheForm
from id2.forms import AbonnementForm
from id2.models import Usager,PieceId,Visite,Service,Abonne,Employe,\
        VisiteProf


def index(request):
    
    contexte = {}
    svce = Service.objects.all().order_by('nom_serv')
    u = Usager.objects.count()
    last_visit = Visite.objects.all().order_by('-date_arrivee')[:20]
    last_inscrit = Usager.objects.all().order_by('-id')[:10]
    #mois en cours
    fus = timezone.get_current_timezone()
    moment = datetime.now(fus)
    debut_mois = moment.replace(day=1,hour=0,minute=0)
    visitCeMois =\
            Visite.objects.filter(date_arrivee__gte=debut_mois)
    #détermination semaine
    # on cherche à avoir la date du premier jour de la semaine
    #et on revient au lundi après 0h00 et qques secondes
    debutSemaine = (moment - timedelta(days=moment.weekday())).replace(
            hour=0,minute=0)
    visitSemaine = Visite.objects.filter(
            date_arrivee__gte=debutSemaine
            )

    contexte = {
            'usager':u,
            'services':svce,
            'derniereVisite': last_visit,
            'dernierInscrit': last_inscrit,
            'visitCeMois' : visitCeMois,
            'visitSemaine': visitSemaine,
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
            cat = form.cleaned_data['categorie']
            company = form.cleaned_data['structure']

            if cat == 'usager':
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
            elif cat == 'employe':
                try :
                    e = Employe.objects.get(nom=n,prenom=p)
                except Employe.DoesNotExist:
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
                    e = Employe(nom=n,sexe=s,prenom=p,
                            piece=piece0,
                            email=em,
                            telephone=tel,
                            structure=company)
                    e.save()
                    contexte = {'message': 'Inscription effectuée'}

                #tout est ok, on revient sur un formulaire vierge
                return HttpResponseRedirect('/ident/inscription/')
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
            nom = form.cleaned_data['nom']
            travailleur = form.cleaned_data['employe']

            if travailleur == False:
                resultat = Usager.objects.filter(nom__icontains=nom).\
                        order_by('nom')
                #on cherche les départs dont les dates ne sont pas
                #encore consignées
                res_depart = Visite.objects.filter(\
                        usager__nom__icontains=nom).\
                        filter(date_deprt=None).\
                        order_by('usager','date_arrivee')
            else :  #Il s'agit donc d'un employé

                resultat = Employe.objects.filter(nom__icontains=nom).\
                        order_by('nom')
                #on cherche les départs dont les dates ne sont pas
                #encore consignées
                res_depart = VisiteProf.objects.filter(\
                        employe__nom__icontains=nom).\
                        filter(date_deprt=None).\
                        order_by('employe','date_arrivee')


            contexte = {'resultat': resultat,
                    'res_depart': res_depart,
                    'travailleur':travailleur,
                    'terme': nom,
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

def visiteProfTraitement(request):
    contexte = {}
    if request.method == 'POST':
        form = VisiteProfForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['nom']
            p = form.cleaned_data['prenom']
            s = form.cleaned_data['structure']
            svce = form.cleaned_data['service']
            m = form.cleaned_data['motif']

            try:
                u = Employe.objects.get(nom=n,prenom=p)
                v = VisiteProf(employe=u,
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

@login_required(login_url='/ident/')
def visite(request,cat_visiteur,visiteur_id):
    """
    A travers cette vue on va consigner automatiquement
    l'heure d'arrivée d'un usager ou d'un employé.
    """

    #cat_visiteur = 0
    if cat_visiteur == 'usager' :
        try :
            u = Usager.objects.get(pk=visiteur_id)
            data = {'nom': u.nom, 'prenom': u.prenom,
                    'categorie': cat_visiteur}
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

    elif cat_visiteur == 'employe' :
        try :
            u = Employe.objects.get(pk=visiteur_id)
            data = {'nom': u.nom, 'prenom': u.prenom,
                    'categorie': cat_visiteur}
            #on lie les données au formulaire
            form = VisiteForm(data)

            contexte = {
                    'form': form,
                    }
            return render(request,'id2/visite.html',contexte)
        except Employe.DoesNotExist:
            message = u'Veuillez enregistrer cet employé au préalable'
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
            c = form.cleaned_data['categorie']

            if c == 'usager':
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


            elif c == 'employe':
                try:
                    e = Employe.objects.get(nom=n,prenom=p)
                    v = VisiteProf(employe = e,
                            service=Service.objects.get(nom_serv=s),
                            type_visit=m)
                    v.save()
                    contexte = {'nom': e.nom,
                            'num': e.id,
                            'structure': e.structure,
                            }
                    return render(request,
                            'id2/visiteur-enregistre.html',\
                            contexte,status=302)

                except Employe.DoesNotExist:
                    # faut trouver un usager qui existe dans la base
                    return HttpResponseRedirect('/ident/recherche')

            else:
                #on considère qu'on a entré une catégorie inconnue
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
            c.date_deprt = timezone.now()
            c.save(update_fields=['date_deprt'])
            return HttpResponseRedirect('/ident/')
    elif etat == 'Non':
        #rien à faire on revient à l'accueil
        return HttpResponseRedirect('/ident/')

def serviceIndex(request,service_id):
    form = RechercheForm()
    #on collecte tous les usagers qui se sont déjà rendus
    #au moins 1 fois dans 1 service donné
    visite = Visite.objects.filter(service=service_id).\
            order_by('-date_arrivee','usager__nom')
    svce_nom = Service.objects.get(pk=service_id).nom_serv
    abonne = Abonne.objects.filter(service=service_id).\
            order_by('-derniere_modif')
    contexte = {'service_nom': svce_nom,
            'service_id':service_id,
            'visite':visite,
            'form':form,
            'abonne':abonne,
            }
    return render(request,'id2/service-index.html',contexte)

def serviceRecherche(request,service_id):
    form = RechercheForm()
    #on collecte tous les usagers qui se sont déjà rendus
    #au moins 1 fois dans 1 service donné
    visite = Visite.objects.filter(service=service_id).\
            order_by('-date_arrivee','usager__nom')
    svce_nom = Service.objects.get(pk=service_id).nom_serv
    contexte = {'service_nom': svce_nom,
            'service_id':service_id,
            'visite':visite,
            'form':form,}
    return render(request,'id2/service-recherche.html',contexte)

def serviceRechercheTraitement(request):
    pass

def serviceAbonnement(request):
    if request.method == 'GET':
        form = RechercheForm(request.GET)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            usager_visit = Usager.objects.filter(nom__icontains=nom)
            if len(usager_visit) == 0:
                message = u"Aucun usager enregistré à ce nom"
                contexte = {'message_erreur': message,
                        'form': form}
                return render(request,'id2/service-index.html',contexte)
            else:
                svce = request.GET['service_id']
                usager_service = \
                        usager_visit.filter(visite__service_id=svce)
                if len(usager_service) == 0:
                    # pas d'usager avec ce nom s'étant rendu au service x
                    return render(request,'id2/service-index.html')
                else:
                    contexte = {'usager_service': usager_service,
                            'service_id': svce,
                            }
                    return render(request,'id2/service-abonnement.html',
                            contexte)

        return HttpResponseRedirect('/ident/')
    else:
        return HttpResponseRedirect('/ident/')

def serviceAbonneAjout(request,service_id,usager_id):
    """Nouvel abonnement ou mise à jour
    """

    u = Usager.objects.get(pk=usager_id)
    service = Service.objects.get(pk=service_id)
    try:
        a = Abonne.objects.get(usager_id=u.id,
                service_id=service.id)
        form = AbonnementForm(initial={'nom':u.nom,
            'prenom':u.prenom,
            'matricule':a.matricule,
            })
    except Abonne.DoesNotExist:
        form = AbonnementForm(initial={'nom':u.nom,
            'prenom':u.prenom,
            })

    contexte = {'form':form,
        'serviceX':service,
        'usager_id':usager_id,
        }

    return render(request,
            'id2/service-abonnement-ajout.html',
            contexte,
            )

def serviceAbonnementTraitement(request):
    if request.method == 'POST':
        form = AbonnementForm(request.POST,request.FILES)
        if form.is_valid():
            n = form.cleaned_data['nom']
            p = form.cleaned_data['prenom']
            mat = form.cleaned_data['matricule']
            expir = form.cleaned_data['expiration']
            photo = form.cleaned_data['photo']
            usager_id = request.POST['usager_id']
            service_id = request.POST['service_id']

            try:
                abo = Abonne.objects.get(usager_id=usager_id,\
                        service_id=service_id)
                abo.expiration = expir
            except Abonne.DoesNotExist:
                abo = Abonne(usager_id=usager_id,
                        service_id=service_id,
                        matricule = mat,
                        photo = photo,
                        expiration = expir,
                        )
                abo.save()
                retour = '/ident/service/%s/' % service_id
                return  HttpResponseRedirect(retour)

            abo.save(update_fields=['expiration','photo'])
            retour = '/ident/service/%s/' % service_id
            return  HttpResponseRedirect(retour)

        else:
            contexte = {
                    'form':form,
                    'message_erreur':u'formulaire non valide',
                    }
            #return HttpResponseRedirect('/ident/')
            return render(request,
                    'id2/service-abonnement-ajout.html',
                    contexte,
                    status=303,
                    )
    else:
        return HttpResponseRedirect(reverse('index'))

def sortie(request):
    logout(request)
    return HttpResponseRedirect('/ident/')
