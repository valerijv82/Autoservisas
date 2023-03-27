from django.contrib.auth.models import User
from .models import OrderReview, UserProfile, Order, OrderLine
from django import forms


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('content', 'order', 'reviewer',)
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = 'date'


# Dėmesio: jei lauke norite nustatyti DateTime lauką, tai yra ir datą ir laiką,
# DateInput klasėje input_type reikšmę pakeiskite iš 'date' į "datetime-local".

class UserOrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car_id', 'data', 'servis']
        widgets = {'useris': forms.HiddenInput(), 'data': DateInput}


class ServiseQuantityPriceForm(forms.ModelForm):
    service_id = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "service"
    }))
    quantity = forms.CharField(widget=forms.TextInput(attrs={
        'type': "number",
        "class": "form-control",
        "placeholder": "quantity"
    }))

    price = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "price"
    }))
    class Meta:
        model = OrderLine
        fields = ['service_id', 'quantity', 'price']
        # widgets = {'order_id': forms.HiddenInput()}
