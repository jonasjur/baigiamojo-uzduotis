from django import forms
from accounts.models import NeatsakytasKlausimas


class KlausimoForma(forms.ModelForm):
    class Meta:
        model = NeatsakytasKlausimas
        fields = ['klausimas']