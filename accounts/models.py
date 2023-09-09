from django import forms
from django.db import models
from django.contrib.auth.models import User



class NeatsakytasKlausimas(models.Model):
    vartotojas = models.ForeignKey(User, on_delete=models.CASCADE)
    klausimas = models.TextField()
    sukurtas = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.klausimas



class AtsakytasKlausimas(models.Model):
    vartotojas = models.ForeignKey(User, on_delete=models.CASCADE)
    klausimas = models.TextField()
    atsakymas = models.TextField()
    sukurtas = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.klausimas
