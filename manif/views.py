from django.shortcuts import render

from .models import Evenement

def index(request):

    contexte = {}
    return render(request,'manif/index.html',contexte)
