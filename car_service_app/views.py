from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm, ProfilisUpdateForm, UserUpdateForm, UserOrderCreateForm, ServiseQuantityPriceForm
from .models import Car, Order, Service, OrderLine


def home(request):
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1  # skaiciuoja sesijas
    context = {
        'num_visits': num_visits
    }
    return render(request, 'home.html', context=context)


def index(request):
    automobiliu_kiekis = Car.objects.all().count()
    atliktu_uzsakymu_kiekis = Order.objects.filter(servis__exact='a').count()
    paslaugu_kiekis = Service.objects.all().count()

    context = {
        'automobiliu_kiekis': automobiliu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'paslaugu_kiekis': paslaugu_kiekis,
    }
    return render(request, 'index.html', context=context)


def automobiliai(request):
    paginator = Paginator(Car.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'cars.html', {'automobiliai': paged_cars})


def automobilis(request, auto_id):
    auto = get_object_or_404(Car, pk=auto_id)
    context = {
        'automobilis': auto
    }
    return render(request, 'car.html', context=context)


class OrdersListView(generic.ListView):
    model = Order
    template_name = "uzsakymai.html"
    paginate_by = 5


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'uzsakymo_details.html'
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
        return super(OrderDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(car_model_id__model__icontains=query)
                                        | Q(customer__icontains=query)
                                        | Q(valstybinis_nr__icontains=query)
                                        | Q(vin_code__icontains=query)
                                        )

    return render(request, 'search.html', {'cars': search_results, 'query': query})


class UserOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(useris=self.request.user).order_by('data')


class UserOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'user_order.html'
    # form_model = ServiseQuantityPriceForm

    # def get_context_data(self, **kwargs):
    #     context = super(UserOrderDetailView, self).get_context_data(**kwargs)
    #     context['order_line'] = OrderLine.objects.filter(order_id=self.get_object())
    #     return context


class CreateLine(LoginRequiredMixin, generic.CreateView):
    model = OrderLine
    fields = ['service_id', 'order_id', 'quantity', 'price']
    # success_url = "/service/my_orders/"
    template_name = 'update_orderline.html'

    def form_valid(self, form):
        form.instance.order_id = get_object_or_404(Order, pk=self.kwargs['uzsakymo_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_order', args=[str(self.kwargs['uzsakymo_pk'])])


class UpdateLine(LoginRequiredMixin, generic.UpdateView):
    model = OrderLine
    fields = ['service_id', 'order_id', 'quantity', 'price']
    # success_url = "/service/my_orders/"
    template_name = 'update_orderline.html'

    def form_valid(self, form):
        form.instance.order_id = get_object_or_404(Order, pk=self.kwargs['uzsakymo_pk'])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('my_order', args=[str(self.kwargs['uzsakymo_pk'])])


class DeleteLine(LoginRequiredMixin, generic.DeleteView):
    model = OrderLine
    success_url = '/service/my_orders/'
    template_name = 'delete_orderline.html'

    def get_success_url(self) -> str:
        return reverse('my_order', args=[str(self.kwargs['line_pk'])])


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


class NewOrderByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    # fields = ['car_id', 'data', 'servis']
    success_url = "/service/my_orders/"
    template_name = 'user_order_form.html'
    form_class = UserOrderCreateForm

    def form_valid(self, form):
        form.instance.useris = self.request.user
        return super().form_valid(form)


class MyOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    fields = ['car_id', 'data', 'servis']
    success_url = "/service/my_orders/"
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.useris = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.useris


class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/service/my_orders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.useris
