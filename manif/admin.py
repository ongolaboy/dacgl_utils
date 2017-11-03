from django.contrib import admin
from manif.models import  Evenement, Participation

class EvenementAdmin(admin.ModelAdmin):
    list_display = ('lieu','intitule','description',
            'debut','fin','duree','ouvert',
    )

admin.site.register(Evenement,EvenementAdmin)
admin.site.register(Participation)
