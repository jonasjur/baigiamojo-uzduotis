from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import KlausimoForma, NeatsakytasKlausimas


def indexView(request):
    return render(request,'index.html')

@login_required()
def dashboardView(request):
    return render (request, 'dashboard.html')

@login_required
def klausimoIvedimoVaizdas(request):
    if request.method == "POST":
        forma = KlausimoForma(request.POST)
        if forma.is_valid():
            klausimas = forma.save(commit=False)
            klausimas.vartotojas = request.user
            klausimas.save()
            return redirect('dashboard')
    else:
        forma = KlausimoForma()
    return render(request, 'klausimo_ivedimo_forma.html', {'forma': forma})


@login_required
def dashboardView(request):

    neatsakyti_klausimai = NeatsakytasKlausimas.objects.filter(vartotojas=request.user)

    if request.method == "POST":
        forma = KlausimoForma(request.POST)
        if forma.is_valid():
            klausimas = forma.save(commit=False)
            klausimas.vartotojas = request.user
            klausimas.save()
            return redirect('dashboard')  # Redirect back to the dashboard after creating a question
    else:
        forma = KlausimoForma()

    return render(request, 'dashboard.html', {'neatsakyti_klausimai': neatsakyti_klausimai, 'forma': forma})

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render (request, 'registration/register.html',{'form':form})

def atvaizduotiKlausima(request, klausimo_id):
    klausimas = NeatsakytasKlausimas.objects.get(id=klausimo_id)
    return render(request, 'klausimo_atvaizdavimas.html', {'klausimas': klausimas})

