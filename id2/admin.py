from django.contrib import admin
from id2.models import Visite,  Usager, Service,PieceId,Abonne

class PieceAdmin(admin.ModelAdmin):
    list_display = ['typePiece','date_expiration']
    list_filter = ['date_expiration','typePiece']
    search_fields = ['code','typePiece']

class UsagerAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','sexe','email','telephone','piece')
    search_fields = ['nom','prenom']
    list_filter = ['sexe']

class VisiteAdmin(admin.ModelAdmin):
    list_display = ('usager','date_arrivee','date_deprt',
            'service','type_visit')
    search_fields = ['usager']
    list_filter = ['service','date_arrivee','date_deprt',
            ]

admin.site.register(Visite,VisiteAdmin)
admin.site.register(PieceId,PieceAdmin)
admin.site.register(Service)
admin.site.register(Abonne)
admin.site.register(Usager,UsagerAdmin)
