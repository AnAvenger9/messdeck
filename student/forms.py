from django import forms
from . models import StudentProfile, StudentAttendance, MenuItems

class StudentProfileUpdateForm(forms.ModelForm):
	bits_id=forms.CharField(label='BITS ID')
	CHOICES = [
        ('Ram', 'Ram'),
        ('Budh', 'Budh'),
        ('Krishna', 'Krishna'),
        ('Gandhi', 'Gandhi'),
        ('Vyas', 'Vyas'),
        ('Shankar', 'Shankar'),
        ('Meera', 'Meera'),
        ('Ashok', 'Ashok'),
        ('Bhagirath', 'Bhagirath'),
        ('RP', 'RP'),
        ('VK', 'VK'),
        ('SR', 'SR'),
        ('CVR', 'CVR'),
    ]
	hostel=forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'custom-dropdown'}))

	class Meta:
		model=StudentProfile
		fields=['bits_id', 'hostel']

class MarkAttendance(forms.ModelForm):
    attendance_mark=forms.BooleanField()

    class Meta:
        model=StudentAttendance
        fields=['attendance_mark']

class RateMenuItem(forms.ModelForm):
    CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),]

    add_rating=forms.ChoiceField(label='Rate the Item on a scale of 1-5', choices=CHOICES, widget=forms.Select(attrs={'class': 'custom-dropdown'}))

    class Meta:
        model=MenuItems
        fields=['add_rating']