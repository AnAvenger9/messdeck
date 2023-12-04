from django.db import models
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import json
from django.conf import settings
import os

# Create your models here.

class StudentProfile(models.Model):

	user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
	google_account=models.OneToOneField(SocialAccount, on_delete=models.CASCADE)
	profile_image=models.ImageField(default='default.jpg', upload_to='profile_pics')
	email_id=models.EmailField(default=None, null=True, blank=True)
	
	name=models.CharField(max_length=200, default=None, null=True, blank=True)
	bits_id=models.CharField(max_length=13, default=None, null=True, blank=True)
	
	hostel=models.CharField(max_length=50, default=None, null=True, blank=True)
	mess=models.CharField(max_length=50, default=None, null=True, blank=True)



	def __str__(self):
		extra_data_dict=self.google_account.extra_data
		return f'{extra_data_dict["name"]}' 



	def save(self, *args, **kwargs):
		import urllib.request
		from PIL import Image

		self.google_account=SocialAccount.objects.get(user=self.user)

		extra_data_dict=self.google_account.extra_data
		self.name=extra_data_dict['name']
		self.email_id=extra_data_dict['email']

		pics_path=os.path.join(settings.MEDIA_ROOT+'/profile_pics')

		urllib.request.urlretrieve(extra_data_dict["picture"], f"{pics_path}/{extra_data_dict['name']}.png")
		self.profile_image=f"{pics_path}/{extra_data_dict['name']}.png"
		

		if self.hostel is not None:
			hostel_mess_relation={'VyasShankar':'Vyas-Shankar Mess',
			'KrishnaGandhi':'Krishna-Gandhi Mess',
			'AshokRP':'Ashok-RP Mess',
			'VKBhagirath':'VK-Bhagirath Mess',
			'RamBudh':'RamBudh-Budh Mess',
			'Meera':'Meera Mess',
			'SR':'SR Mess',
			'CVR':'CVR Mess',
			}
			for i in hostel_mess_relation:
				if self.hostel in i:
					self.mess=hostel_mess_relation[i]


		super().save(*args, **kwargs)


	

class Complaint(models.Model):
	student=models.ForeignKey(StudentProfile, on_delete=models.CASCADE, default=None, null=True)
	title=models.CharField(max_length=255,default=None)
	complaint=models.TextField()
	date_posted=models.DateTimeField(default=timezone.now)
	author_id=models.CharField(max_length=50,default=None, null=True)
	author=models.CharField(max_length=20, default=None, null=True)
	image=models.ImageField(default='default.jpg', upload_to='complaint_pics')

	def __str__(self):
		return self.title

	def save(self,*args, **kwargs):
		self.author_id=self.student.bits_id
		self.author=self.student.name
		self.mess=self.student.mess
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('complaint-detail', kwargs={'pk':self.pk})

class MenuItems(models.Model):
	date_to_be_served=models.CharField(max_length=10, default=None, null=True)
	meal=models.CharField(max_length=9, default=None, null=True)
	item_name=models.CharField(max_length=255, default=None, null=True)
	ratings=models.TextField(default="", blank=True)
	avg_rating=models.IntegerField(default=0, null=True)

	def save(self, *args, **kwargs):
		rating_sum=0
		if self.ratings!="":
			for rating in self.ratings:
				rating_sum+=int(rating)
				self.avg_rating=(rating_sum)/len(self.ratings)
		super().save(*args,**kwargs)


class ManagerStaff(models.Manager):
    def filter_or_create(self, **kwargs):
        # Attempt to filter the model based on the provided kwargs
        queryset = self.filter(**kwargs)

        if queryset.exists():
            # Return the existing instance if it exists
            return queryset.first(), False
        else:
            # Create a new instance if it doesn't exist
            instance = self.create(**kwargs)
            return instance, True


class StudentAttendance(models.Model):
	student=models.ForeignKey(User, on_delete=models.CASCADE)
	date=models.CharField(max_length=10, default=None, null=True)
	meal=models.CharField(max_length=9, default=None, null=True)
	attendance_mark=models.BooleanField(default=False)

	objects=ManagerStaff()
	def __str__(self):
		return f'Attendance for {self.student.studentprofile.bits_id} on date {self.date}, meal:{self.meal}'


class StudentBill(models.Model):
	student=models.OneToOneField(User, on_delete=models.CASCADE)
	lunch=models.IntegerField()
	dinner=models.IntegerField()
	breakfast=models.IntegerField()

	def __str__(self):
		return f'{self.student.studentprofile.bits_id}'

	def save(self, *args, **kwargs):
		self.lunch=StudentAttendance.objects.filter(student=self.student, meal="LUNCH", attendance_mark=True).count()
		self.breakfast=StudentAttendance.objects.filter(student=self.student, meal="BREAKFAST", attendance_mark=True).count()
		self.dinner=StudentAttendance.objects.filter(student=self.student, meal="DINNER", attendance_mark=True).count()
		super().save(*args, **kwargs)

