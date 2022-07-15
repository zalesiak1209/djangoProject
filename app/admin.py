# Django
from django.contrib import admin

# Project
# Register your models here.
from app.models import Kategoria
from app.models import Ogloszenie

admin.site.register(Ogloszenie)
admin.site.register(Kategoria)
