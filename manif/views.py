from django.shortcuts import render,HttpResponseRedirect
from django.utils import timezone
from id2.models import Usager,PieceId,Visite,Service
from .forms import ParticipationForm,NomForm
from .models import Participation

from .models import Evenement, Participation

def index(request):

    contexte = {}
    manifs = Evenement.objects.filter(ouvert=True)
    contexte = {'manifs': manifs,
            }
    return render(request,'manif/index.html',contexte)

def consigne(request):
    formulaire_participation = ParticipationForm()
    contexte = {'formulaire_participation': formulaire_participation,}
    return render(request,'manif/consigne-individuelle.html',contexte)

def consigne21(request):
    formulaire_participation = NomForm()
    contexte = {'formulaire_participation': formulaire_participation,}
    return render(request,'manif/consigne-individuelle21.html',contexte)

def rechercheTraitement(request):
    contexte = {}
    if request.method == 'GET':
        form = NomForm(request.GET)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            s = form.cleaned_data['sexe']

            resultat = Usager.objects.filter(nom__icontains=nom).\
                    filter(sexe=s).order_by('nom')
            data = {'nom':nom, 'prenom':prenom,'sexe':s,}
            if resultat.count() == 0:
                form = ParticipationForm(data)
                contexte = {'form': form,}
                return render(request,
                        'manif/consigne-individuelle23.html',
                        contexte)
            else:
                contexte = {'resultat': resultat,
                        'data': data,}
                return render(request,
                        'manif/consigne-individuelle22.html',
                        contexte)

def consigneUsager(request,user_id):
    visiteur = Usager.objects.get(pk=int(user_id))
    data = {'nom':visiteur.nom,
            'prenom':visiteur.prenom,
            'sexe':visiteur.sexe,
            }
    formulaire_participation = ParticipationForm(data)
    contexte = {'formulaire_participation':formulaire_participation,}
    return render(request,'manif/consigne-individuelle.html',contexte)

def consigneTraitement(request):
    contexte = {}
    if request.method == 'POST':
        form = ParticipationForm(request.POST)
        if form.is_valid():
            e = form.cleaned_data['evenement']
            n = form.cleaned_data['nom']
            p = form.cleaned_data['prenom']
            s = form.cleaned_data['sexe']
            em = form.cleaned_data['courriel']
            comm = form.cleaned_data['commentaire']

            try:
                u = Usager.objects.get(nom=n,prenom=p,sexe=s)
            except Usager.DoesNotExist:
                #on attribue 'autre' comme type de carte
                piece0 = PieceId(typePiece='autre')
                piece0.save()
                u = Usager(nom=n,prenom=p,sexe=s,piece=piece0)
                u.save()
            if em != '':
                if u.email == '':
                    u.email = em
                    u.save(update_fields=['email'])
            particip = Participation(usager=u,evenement=e,
                    commentaire=comm)
            particip.save()
            v = Visite(usager=u,
                    service=Service.objects.get(nom_serv=e.lieu),
                    type_visit=e.intitule,
                    date_arrivee=timezone.now())
            v.save()
            message = "Merci %s de vous être enregistré" % (u.nom)

            return HttpResponseRedirect('/manif/')
        else:
            contexte = {'message': 'Veuillez revérifier votre saisie',
                    'form': form,
                    }
            return render(request,
                    'manif/consigne-individuelle.html',
                    contexte,status=303)
    else :
        form = ParticipationForm()
        contexte = {'message': 'Veuillez recommencer svp'}
        return render(request,'manif/consigne-individuelle.html',
                contexte)

def bilan(request):
    contexte = {}
    if Evenement.objects.all != None:
        ev = Evenement.objects.all()
        ev_liste = {}
        for ev1 in ev:
            particip_total = ev1.participant.all()
            ev_liste[ev1.id] = (ev1.intitule,
                    ev1.debut, ev1.duree(),
                    particip_total.all().count(),
                    particip_total.filter(sexe='H').count(),
                    particip_total.filter(sexe='F').count(),
                    )
        contexte = {'ev_all':ev,'ev_critere':ev_liste}

    else: contexte = {'message_erreur':"Il n'y a pas d'évènements"}

    return render(request,'manif/bilan.html',contexte)


def  bilanDetaille(request,bilan_id):

    contexte = {}
    presents = Participation.objects.filter(evenement=bilan_id).\
            order_by('usager__nom')
    presents_total = presents.count()
    present_H = presents.filter(usager__sexe='H').count()
    present_F = presents.filter(usager__sexe='F').count()
    ev = Evenement.objects.get(pk=bilan_id)

    contexte = {'presents': presents,
            'presents_total': presents_total,
            'present_H': present_H,
            'present_F': present_F,
            'ev': ev}

    return render(request,'manif/bilan-detaille.html',contexte)
