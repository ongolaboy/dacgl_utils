#-*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from Identification.forms import ConnexionForm, ContactForm

from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from Identification.models import Service, Visite, Usager

from django.contrib.auth import authenticate, login

# Create your views here.
#vue correspondant a la connexion d'un utilisateur sur le site
def connexion(request):
    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes

            if user:  # Si l'objet renvoyé n'est pas None
                 #visites = Visite.objects.all()[:10]
                 #context = { 'username': username,
                             #'visites': visites }
                 login(request, user)# nous connectons l'utilisateur
                 context = {}
                 return render_to_response('identification/home.html', context)
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
        #Bien preciser le chemin pour acceder au templates.
    return render(request, 'identification/connexion.html', locals())
 
 #vue correspondant a la deconnexion d'un utilisateur   
def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))

 #vue correspondant a la page d'accuiel   
def home(request):
    visites = Visite.objects.all()
    return render_to_response('identification/home.html', {'visites': visites})
 
#vue correspondant a enregistrement une visite et un usager .... inachevée
def visiteusager(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(home))
        else:
            form = ContactForm()  
    return render(request, 'Identification/visiteusager.html', locals())
