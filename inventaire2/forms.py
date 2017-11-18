from django import forms
from .models import Implantation

class inventaireLegacyForm(forms.Form):
    fichier = forms.FileField()

class implantationForm(forms.Form):
    implantationX = forms.ModelChoiceField(label='Implantation',
            queryset=Implantation.objects.all())
