from django.contrib import admin
from .models import CNI
# Register your models here.
@admin.register(CNI)
class PostAdmin(admin.ModelAdmin):
    list_display = ('NumeroCni','date_naissance','nom')
    