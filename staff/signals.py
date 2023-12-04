from django.db.models.signals import post_save, Signal
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import StaffProfile, MessMenu

@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
	if created:
		StaffProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_staff_profile(sender, instance, **kwargs):
	try:
		instance.staffprofile.save()
	except:
		pass

mess_menu_uploaded = Signal()

@receiver(post_save, sender=MessMenu)
def handle_menu_upload(sender, instance, **kwargs):
	mess_menu_uploaded.send(sender=sender, instance=instance)