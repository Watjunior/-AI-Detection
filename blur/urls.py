from django.urls import path
from .views import upload_image,home,about,modele,choix,contact

urlpatterns =[
    path('', home, name='home'), 
    path('upload_image', upload_image, name='upload_image'),
    path('about', about, name='about'),
    path('modele', modele, name='modele'),
    path('choix', choix, name='choix'),
    path('contact', contact, name='contact'),


]