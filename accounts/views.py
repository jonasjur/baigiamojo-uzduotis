
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import KlausimoForma
from accounts.models import NeatsakytasKlausimas, AtsakytasKlausimas

# Apibrėžiama peržiūros funkcija pagrindiniam puslapiui
def indexView(request):
    return render(request, 'index.html')

# Apibrėžiama peržiūros funkcija skydeliui, kuriame išvardinami neatsakyti ir atsakyti klausimai
@login_required
def dashboardView(request):
    # Gaunami visi neatsakyti ir atsakyti klausimai iš duomenų bazės
    neatsakyti_klausimai = NeatsakytasKlausimas.objects.all()
    atsakyti_klausimai = AtsakytasKlausimas.objects.all()

    if request.method == "POST":
        # Tvarkomas formos pateikimas, jei tai yra POST užklausa
        forma = KlausimoForma(request.POST)
        if forma.is_valid():
            klausimas = forma.save(commit=False)
            klausimas.vartotojas = request.user
            klausimas.save()
            return redirect('dashboard')  # Nukreipimas į skydelį po klausimo išsaugojimo

    else:
        # Sukuriamas naujas formos pavyzdys GET užklausoms
        forma = KlausimoForma()

    # Atvaizduojamas skydelio šablonas ir perduodami gauti klausimai ir forma į šabloną
    return render(request, 'dashboard.html', {'neatsakyti_klausimai': neatsakyti_klausimai, 'atsakyti_klausimai': atsakyti_klausimai, 'forma': forma})

# Apibrėžiama peržiūros funkcija naujo klausimo įvedimui
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

# Apibrėžiama registracijos peržiūros funkcija
def registerView(request):
    if request.method == "POST":
        # Tvarkomas vartotojo registracijos formos pateikimas
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Išsaugojami vartotojo registracijos duomenys
            return redirect('login_url')  # Nukreipimas į prisijungimo puslapį po sėkmingos registracijos
    else:
        # Sukuriamas naujas vartotojo registracijos formos pavyzdys GET užklausoms
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Apibrėžiama peržiūros funkcija konkrečiam klausimui peržiūrėti ir tvarkyti
@login_required
def atvaizduotiKlausima(request, klausimo_id):
    # Gaunamas konkretus neatsakytas klausimas pagal jo ID
    klausimas = NeatsakytasKlausimas.objects.get(id=klausimo_id)

    if request.method == "POST":
        atsakymas_text = request.POST.get('atsakymas')
        if atsakymas_text:
            # Sukuriamas naujas atsakytas klausimas ir susiejamas su vartotoju
            AtsakytasKlausimas.objects.create(
                vartotojas=klausimas.vartotojas,
                klausimas=klausimas.klausimas,
                atsakymas=atsakymas_text,
                atsakymo_vartotojas=request.user,
            )

            klausimas.delete()  # Ištrinamas pradinis neatsakytas klausimas
            return redirect('dashboard')  # Nukreipimas į skydelį

    return render(request, 'klausimo_atvaizdavimas.html', {'klausimas': klausimas})

# Apibrėžiama peržiūros funkcija atsakymui patikti/nebepatikti
def like_answer(request, answer_id):
    answer = AtsakytasKlausimas.objects.get(id=answer_id)
    already_liked = answer.liked_by.filter(id=request.user.id).exists()
    # Patikrinama, ar vartotojas jau patiko atsakymą

    if already_liked:
        answer.liked_by.remove(request.user)  # Pašalinamas vartotojo patinka, jei jis jau buvo patikęs atsakymą
    else:
        answer.liked_by.add(request.user)  # Pridedamas vartotojo patinka, jei jis dar nepatiko atsakymo

    return redirect('dashboard')  # Nukreipimas atgal į skydelį
