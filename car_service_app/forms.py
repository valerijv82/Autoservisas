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
