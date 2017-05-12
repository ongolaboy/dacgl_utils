#-*- coding: utf-8 -*-

from django import forms

from id2.models import Service

class InscriptionForm(forms.Form):
    """
    Ce formulaire s'occupe des inscriptions dans le syst�me.
    Et donc pour toutes les personnes pas encore identifi�es
    """
    SEXE = (('H',u'homme'),('F',u'femme'),)

    PIECE = (
            ('cni',u'CNI'),
            ('passeport',u'passeport'),
            ('recepisse',u'recepisse'),
            ('autre',u'autre carte'),
            )

    nom = forms.CharField(max_length=50)
    prenom = forms.CharField(max_length=150,required=False)
    sexe = forms.ChoiceField(choices=SEXE)
    typePiece = forms.ChoiceField(label='Type de piece',choices=PIECE)
    code = forms.CharField(max_length=60,
            help_text=u"Numero ou identifiant de la piece.")
    date_expiration=forms.DateField(label=u"Date d'expiration",
            required=False,
            help_text="Format<br>DD/MM/YYYY",
            )
    email = forms.EmailField(label=u"Adresse electronique",
            required=False)
    telephone = forms.IntegerField(help_text=u"Num de telephone",\
            required=False)

class VisiteForm(forms.Form):
    """
    Enregistrement des visites d'usager
    """

    nom = forms.CharField()
    prenom = forms.CharField()
    service = forms.ModelChoiceField(\
            queryset=Service.objects.all().order_by('nom_serv'))
    motif = forms.CharField(widget=forms.Textarea,
            initial=u"visite")

class RechercheForm(forms.Form):
    nom = forms.CharField()
