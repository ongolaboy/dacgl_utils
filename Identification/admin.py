from django.contrib import admin
from .models import Visite, Employe, Usager, Service

# Register your models here.
admin.site.register(Visite)
admin.site.register(Service)
admin.site.register(Usager)

admin.site.register(Employe)
