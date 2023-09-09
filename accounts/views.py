from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.forms import KlausimoForma
from accounts.models import  NeatsakytasKlausimas, AtsakytasKlausimas


def indexView(request):
    return render(request, 'index.html')


@login_required
def dashboardView(request):
    neatsakyti_klausimai = NeatsakytasKlausimas.objects.all()
    atsakyti_klausimai = AtsakytasKlausimas.objects.all()

    if request.method == "POST":
        forma = KlausimoForma(request.POST)
        if forma.is_valid():
            klausimas = forma.save(commit=False)
            klausimas.vartotojas = request.user
            klausimas.save()
            return redirect('dashboard')

    else:
        forma = KlausimoForma()

    return render(request, 'dashboard.html', {'neatsakyti_klausimai': neatsakyti_klausimai, 'atsakyti_klausimai': atsakyti_klausimai, 'forma': forma})


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


def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def atvaizduotiKlausima(request, klausimo_id):
    klausimas = NeatsakytasKlausimas.objects.get(id=klausimo_id)


    if request.method == "POST":
        atsakymas = request.POST.get('atsakymas')
        if atsakymas:

            AtsakytasKlausimas.objects.create(
                vartotojas=request.user,
                klausimas=klausimas.klausimas,
                atsakymas=atsakymas,
            )

            klausimas.delete()
            return redirect('dashboard')

    return render(request, 'klausimo_atvaizdavimas.html', {'klausimas': klausimas})


def like_answer(request, answer_id):
    answer = AtsakytasKlausimas.objects.get(id=answer_id)
    already_liked = answer.liked_by.filter(id=request.user.id).exists()

    if already_liked:
        answer.liked_by.remove(request.user)
    else:
        answer.liked_by.add(request.user)

    return redirect('dashboard')

