#-*- coding: utf-8 -*-

from django import forms

from id2.models import Service,Societe

class InscriptionForm(forms.Form):
    """
    Ce formulaire s'occupe des inscriptions dans le systeme.
    Et donc pour toutes les personnes pas encore identifiees
    """
    SEXE = (('H',u'homme'),('F',u'femme'),)

    CATEGORIE = (('usager',u'usager'),('employe',u'employe'),)

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
    categorie = forms.ChoiceField(label='Type de visiteur',\
            choices=CATEGORIE)
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
    structure = forms.ModelChoiceField(\
            help_text=u"Si employe, de quelle structure ?",
            queryset=Societe.objects.all().order_by('nom'),
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
    categorie = forms.CharField(help_text="Type de visiteur")

class RechercheForm(forms.Form):
    nom = forms.CharField()
    employe = forms.BooleanField(help_text=\
            u"<br>Veuillez cocher s'il s'agit d'un employe",
            required=False)

class AbonnementForm(forms.Form):
    nom = forms.CharField()
    prenom = forms.CharField()
    matricule = forms.CharField(max_length=60,
            #FIXME : pourquoi avec les accents ça génère une erreur ?
            #(unicode error) 'utf8' codec can't decode byte 0xe9 ...
            help_text=u"Code genere suivants les regles du service")
    photo = forms.ImageField(required=False)
    expiration = forms.DateField()
