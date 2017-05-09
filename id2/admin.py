from django.contrib import admin
from id2.models import Visite,  Usager, Service,PieceId

class UsagerAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','sexe','email','telephone')
    search_fields = ['nom','prenom']

class VisiteAdmin(admin.ModelAdmin):
    list_display = ('usager','date_arrivee','date_deprt',
            'service','type_visit')
    search_fields = ['usager']
    list_filter = ['service','date_arrivee','date_deprt',
            ]

admin.site.register(Visite,VisiteAdmin)
admin.site.register(PieceId)
admin.site.register(Service)
admin.site.register(Usager,UsagerAdmin)
