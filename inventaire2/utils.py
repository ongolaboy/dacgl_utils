# -*- coding: utf-8 -*-
"""Fonctions utiles à la gestion des inventaires
"""

import random
from string import ascii_uppercase, digits

from .models import Piece

def code_aleatoire(pas=5):
    """Un code inventaire temporaire.

    Au cas où il n'existe pas de code d'inventaire,cette fonction
    permet d'attribuer un code qui pourra éventuellement être changé
    par la suite
    """

    aleas = ascii_uppercase + digits
    nbr_alea = 'X '
    trouve = False
    while trouve == False:

        while pas != 0:
            nbr_alea += random.choice(alea)
            pas -=  1

        try:
            Piece.objects.get(code_inventaire=nbr_alea)
        except:
            trouve = True
    return nbr_alea
