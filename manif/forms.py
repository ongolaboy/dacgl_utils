from django import forms
from .models import Participation, Evenement


SEXE = (('H',u'homme'),('F',u'femme'),)

class ParticipationForm(forms.Form):
    evenement = forms.ModelChoiceField(help_text="Quel évènement?",
            queryset=Evenement.objects.filter(ouvert=True))
    nom = forms.CharField()
    prenom = forms.CharField()
    sexe = forms.ChoiceField(choices=SEXE)
    courriel = forms.EmailField(required=False,
            help_text="si vous souhaitez recevoir nos annonces")
    commentaire = forms.CharField(widget=forms.Textarea,
            help_text="Avez-vous un avis/remarque à effectuer ?",
            required=False)
