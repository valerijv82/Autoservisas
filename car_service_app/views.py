from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator

from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm, ProfilisUpdateForm, UserUpdateForm

from .models import CarModel, Car, Order, OrderLine, Service


def home(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1  # skaiciuoja sesijas
    context = {
        'num_visits': num_visits
    }
    return render(request, 'home.html', context=context)


def index(request):
    automobiliu_kiekis = Car.objects.all().count()
    atliktu_uzsakymu_kiekis = Order.objects.all().count()
    # paslaugu_kiekis = Service.objects.filter(name__exact='p').all().count()
    paslaugu_kiekis = Service.objects.all().count()
    servisu_kiekis = Order.objects.all()

    context = {
        'automobiliu_kiekis': automobiliu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'paslaugu_kiekis': paslaugu_kiekis,
        'servisu_kiekis': servisu_kiekis,
    }
    return render(request, 'index.html', context=context)


def automobiliai(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'cars.html', {'automobiliai': paged_authors})

    # autos = Car.objects.all()
    # context = {
    #     'automobiliai': autos
    # }
    # return render(request, 'cars.html', context=context)


def automobilis(request, auto_id):
    auto = Car.objects.get(pk=auto_id)
    context = {
        'automobilis': auto
    }
    return render(request, 'car.html', context=context)


class UzsakymaiView(generic.ListView):
    model = Order
    template_name = "uzsakymai.html"
    paginate_by = 2


class UzsakymaiDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'uzsakymai_detail.html'
    form_class = OrderReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('uzsakymas', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(UzsakymaiDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(car_model_id__model__icontains=query)
                                        | Q(customer__icontains=query)
                                        | Q(valstybinis_nr__icontains=query)
                                        | Q(vin_code__icontains=query)
                                        )

    return render(request, 'search.html', {'cars': search_results, 'query': query})


class LoadCarsByListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'user_order.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(useris=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilis atnaujintas')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'user_profile.html', context=context)

# class OrderDetailView(FormMixin, generic.DetailView):
#     model = Order
#     template_name = 'uzsakymai_detail.html'
#     form_class = OrderReviewForm
#
#     # nurodome, kur atsidursime komentaro sėkmės atveju.
#     def get_success_url(self):
#         return reverse('my_orders', kwargs={'pk': self.object.id})
#
#     # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
#     def form_valid(self, form):
#         form.instance.order = self.object
#         form.instance.reviewer = self.request.user
#         form.save()
#         return super(OrderDetailView, self).form_valid(form)
