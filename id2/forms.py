#-*- coding: utf-8 -*-

from django import forms

class InscriptionForm(forms.Form):
    """
    Ce formulaire s'occupe des inscriptions dans le système.
    Et donc pour toutes les personnes pas encore identifiées
    """
    SEXE = (('H',u'homme'),('F',u'femme'),)

    PIECE = (
            ('passeport',u'passeport'),
            ('cni',u'CNI'),
            ('recepisse',u'recepisse'),
            ('autre',u'autre carte'),
            )

    nom = forms.CharField(max_length=50)
    sexe = forms.ChoiceField(choices=SEXE)
    prenom = forms.CharField(max_length=150,required=False)
    typePiece = forms.ChoiceField(choices=PIECE)
    code = forms.CharField(max_length=60,
            help_text=u"Numero ou identifiant de la piece.")
    date_expiration=forms.DateField(label=u"Date d'expiration",
            required=False,help_text="Format<br>YYYY/MM/DD",
            input_formats = ['%Y/%m/%d'])
    email = forms.EmailField(label=u"Adresse electronique",
            required=False)
    telephone = forms.IntegerField(help_text=u"Num de telephone",\
            required=False)
