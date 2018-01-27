from django.conf.urls import url
from . import views

app_name = "bureautique"

urlpatterns = [
     url(r'^retrait/$', views.retrait, name='retrait'),
     url(r'^consommable/$', views.consommable, name='consommable'),
     url(r'^$', views.home, name='index'),
]
