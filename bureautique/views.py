# -*- coding:utf-8 -*-

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render_to_response,render
from bureautique.models import Consommable,Imprimante,RetraitConsommable,\
        Personnel

def home(request):
#    req = Consommable.objects.filter(modele__exact=self.modele).filter(disponible__exact=True).count()
    modeles = ['05A','920XL','950XL','951XL','933 XL',\
            '932 XL','951 XL','950 XL']
    stock = {}
    imprimantes_modele = []
    imprimante_emplacement = []
    usage_imprimante = {}
    employer = {}

    for i in modeles :
        for j in Consommable.NOM_COULEUR :
            composant = "%s %s" % (i,j[0])
            v =\
            Consommable.objects.filter(modele=i).filter(couleur=j[0]).filter(disponible=True).count()
            #if v > 0 :
            stock[composant] = v

    imprimantes = Imprimante.objects.order_by(\
            'modele','emplacement').all()

    derniers_retraits =\
    RetraitConsommable.objects.order_by('-date_retrait')[:5]

    #avoir des stats sur l'usage des imprimantes
    for k in Imprimante.objects.all():
        imprimantes_modele.append(k.modele)
        place = "%s %s" % (k.modele,k.emplacement)

        usage_imprimante[place] =\
    RetraitConsommable.objects.filter(\
    imprimante_utilisee__modele=k.modele).filter(\
    imprimante_utilisee__emplacement=k.emplacement).count()

    for k in Personnel.objects.all():
        frequence =\
        RetraitConsommable.objects.filter(demandeur__nom=k.nom).count()
        if frequence == 0 : 
            pass
        else :
            employer[k.nom] = frequence

    contexte = {'stock' : stock,
            'imprimantes': imprimantes,
            'derniers_retraits' : derniers_retraits,
            'usage_imprimante' : usage_imprimante,
            'employer' : employer,
            }
    
    return render(request,'bureautique/index.html',contexte)
#    return render_to_response('bureautique/index.html',
#            {'imprimantes':imprimantes},
#            )

def consommable(request):
    consommable_dispo = Consommable.objects.filter(disponible__exact=True)
    return render_to_response('bureautique/consommable.html',
            {'consommable_dispo':consommable_dispo},
            )

def consommable_detail(request,consommable_modele):
    """
    Il s'agit des consommables d'un modèle précis ET
    qui sont disponibles
    """

    consommable_dispo = Consommable.objects.filter(disponible__exact=True)
    consommable_dispo = consommable_dispo.filter(\
            modele__exact=consommable_modele)
    return render_to_response('bureautique/consommable_detail.html',
            {'consommable_dispo':consommable_dispo},
            )

def retrait(request):
    retrait_list = RetraitConsommable.objects.all()
    paginator_ret = Paginator(retrait_list,30)
    page = request.GET.get('page')
    try:
        retrait_p = paginator_ret.page(page)
    except PageNotAnInteger:
        retrait_p = paginator_ret.page(1)
    except EmptyPage:
        retrait_p = paginator_ret.page(paginator.num_pages)

    contexte = {
            'retrait_p': retrait_p,
            'retrait_list': retrait_list,
            }

    return render(request,'bureautique/retrait.html',contexte)
