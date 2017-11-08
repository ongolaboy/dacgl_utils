from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render,HttpResponseRedirect
from id2.models import Usager,PieceId
from .forms import ParticipationForm
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
