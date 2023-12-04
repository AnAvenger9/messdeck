from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile


class StaffRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StaffProfileUpdateForm(forms.ModelForm):
    psrn_no=forms.CharField(label='PSRN No.')

    class Meta:
        model = StaffProfile
        fields = ['psrn_no']

class StaffUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label= 'Email')

    class Meta:
        model = User
        fields = ['username','email']


class CalculateBill(forms.Form):
    search_query = forms.CharField(max_length=255, required=False)


class ItemsSortForm(forms.Form):
    CHOICES=[
        ('-avg_rating', 'Avg. Rating Highest to Lowest'),
        ('avg_rating', 'Avg. Rating Lowest to Highest'),
        ('-date_to_be_served', 'Date Served Newest to Oldest'),
        ('date_to_be_served', 'Date Served Oldest to Newest'),
    ]
    sortby = forms.ChoiceField(label="Sort Items By ", choices=CHOICES, required=False)