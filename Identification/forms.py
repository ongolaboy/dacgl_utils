#-*- coding: utf-8 -*-
from django import forms
from .models import Usager, Visite, Profil, Service
#formulaire de connexion
class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

#formulaire enregistrement usager et une visite ..... inachevé
class ContactForm(forms.Form):
    nom_usgr = forms.CharField(max_length=50)
    CNI = forms.IntegerField()
    email = forms.EmailField()
    telephone = forms.IntegerField()
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all())
