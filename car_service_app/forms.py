from django.contrib.auth.models import User
from .models import OrderReview, UserProfile, Order
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

