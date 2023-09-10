
from django.db import models
from django.contrib.auth.models import User


# Apibrėžiamas Django modelis neatsakytų klausimų saugojimui.
class NeatsakytasKlausimas(models.Model):
    vartotojas = models.ForeignKey(User, on_delete=models.CASCADE)
    klausimas = models.TextField()
    sukurtas = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.klausimas

# Apibrėžiamas Django modelis atsakytų klausimų saugojimui.

class AtsakytasKlausimas(models.Model):
    vartotojas = models.ForeignKey(User, on_delete=models.CASCADE)
    klausimas = models.TextField()
    atsakymas = models.TextField()
    atsakymo_vartotojas = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)  # Add this field
    sukurtas = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    def __str__(self):
        return self.klausimas
