from django.db import models
from django.contrib.auth.models import User
from student.models import StudentProfile, StudentAttendance
from django.db.models.signals import Signal



# Create your models here.
class StaffProfile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	psrn_no=models.CharField(max_length=15, default=None, null=True)

	def __str__(self):
		return f'{self.user.username}'

class MessMenu(models.Model):
	excel_file=models.FileField(upload_to='uploads/mess_menu/')
	uploaded_at=models.DateTimeField(auto_now_add=True)





