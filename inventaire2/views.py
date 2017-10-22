import csv

from django.http import HttpResponse
from django.shortcuts import render

from .models import Piece

# Create your views here.

def index(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sortie.csv"'
    
    total_piece = Piece.objects.all()
    writer = csv.writer(response)

    writer.writerow(['Intitule','date_acquisition',
            'code_inventaire','commande_coda'])
    for piece in Piece.objects.all():
        writer.writerow([piece.intitule, piece.date_acquisition,
                piece.code_inventaire, piece.commande_coda])

#    writer.writerow(['Premiere ligne','un','deu','trois'])
#    writer.writerow(['deuxieme ligne','cinquo','deu','mais ou ai je la tete'])
    return response
#    total_piece = Piece.objects.all()
#    return render(request,'inventaire2/index.html',
#            {'total_piece': total_piece})
