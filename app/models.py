# Django
from django.contrib.auth import get_user_model

User = get_user_model()

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class Kategoria(models.Model):
    kat = [
        ('Motoryzacja', 'Motoryzacja'), ('Rolnictwo', 'Rolnictwo'), ('Materiały Budowlane', 'Materiały Budowlane'),
        ('Elektronika', 'Elektronika'), ('Praca', 'Praca'), ('Dom i Ogród', 'Dom i Ogród'),
        ('Nieruchomości', 'Nieruchomości'),
        ('Wynajem', 'Wynajem'), ('Sport', 'Sport'), ('Oddam', 'Oddam'), ('Zwierzęta', 'Zwierzęta'), ('Moda', 'Moda'),
        ('Inne', 'Inne')]
    name = models.CharField(max_length=255, choices=kat, null=False, unique=True, verbose_name='Kategoria')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CustomUser(AbstractUser):
    pass

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = True


class Ogloszenie(models.Model):
    nazwa_ogloszenia = models.CharField(max_length=50, null=False)
    krotki_opis_ogloszenia = models.CharField(max_length=50, null=False)
    tresc_ogloszenia = models.CharField(max_length=500, null=False)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    rok_produkcji = models.CharField(max_length=4)
    miejscowosc = models.CharField(max_length=255)
    numer_telefonu = models.CharField(max_length=9, null=False)
    data_dodania = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=12, verbose_name='Cena', decimal_places=2)
    zdjecie = models.FileField(upload_to='upload_images/', blank=True, default='upload_images/foto.jpg')

    def __str__(self):
        return self.nazwa_ogloszenia

    class Meta:
        ordering = ['-data_dodania']
