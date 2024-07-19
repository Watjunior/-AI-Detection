from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

from django.db import models

class CNI(models.Model):
    nom = models.CharField(max_length=20 ,default=None)
    prenom = models.CharField(max_length=20,default=None)
    lieu_naissance = models.CharField(max_length=20, default='Inconnu')
    date_naissance = models.DateField(auto_now=False, default='1999-01-01')
    profession = models.CharField(max_length=20,default=None)
    sexe = models.CharField(max_length=2,default=None)
    addresse = models.CharField(max_length=20, default=None)
    NumeroCni = models.PositiveIntegerField(default=None)

    def __str__(self) -> str:
        return self.nom


