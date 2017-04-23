from django.contrib import admin
from Identification.models import Visite,  Usager, Service,PieceId

# Register your models here.
admin.site.register(Visite)
admin.site.register(PieceId)
admin.site.register(Service)
admin.site.register(Usager)
