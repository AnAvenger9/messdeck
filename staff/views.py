from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import StaffRegisterForm, StaffProfileUpdateForm, StaffUserUpdateForm, CalculateBill, ItemsSortForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import login_required
from student.models import Complaint, StudentBill, StudentProfile, StudentAttendance, MenuItems
from .models import MessMenu
from django.utils import timezone
from datetime import datetime, time, timedelta
import pandas as pd
from django.conf import settings
import os
import csv
# Create your views here.


def dashboard(request):
	attendances=[]
	for i in range(1,6):
		date=str((timezone.now().astimezone(timezone.get_current_timezone())-timedelta(days=i)).date())
		breakfast_attendance=StudentAttendance.objects.filter(date=date, meal='BREAKFAST',attendance_mark=True).count()
		lunch_attendance=StudentAttendance.objects.filter(date=date, meal='LUNCH',attendance_mark=True).count()
		dinner_attendance=StudentAttendance.objects.filter(date=date, meal='DINNER',attendance_mark=True).count()
		attendances.append({'date':date, 'breakfast':breakfast_attendance,'lunch':lunch_attendance, 'dinner':dinner_attendance})

	return render(request, 'staff/dashboard.html', {'attendances':attendances})


def register(request):
	if request.method == 'POST':
		form = StaffRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('staff-dashboard')
	else:
		form=StaffRegisterForm()
	return render(request, 'staff/register.html', {'form':form})

class CustomLogoutView(LogoutView):

    def get_success_url(self):
        # Get the 'next' parameter from the URL or use a default redirect URL
        redirect_url = self.request.GET.get('next', 'http://localhost:8000/staff')
        return redirect_url

class CustomLoginView(LoginView):

    def get_success_url(self):
        # Get the 'next' parameter from the URL or use a default redirect URL
        redirect_url = self.request.GET.get('next', 'http://localhost:8000/staff')
        return redirect_url


@login_required
def profile(request):
	return render(request, 'staff/profile.html')

@login_required
def profile_update(request):
	if request.method == 'POST':
		p_form = StaffProfileUpdateForm(request.POST, instance=request.user.staffprofile)
		u_form = StaffUserUpdateForm(request.POST, instance=request.user)
		if p_form.is_valid() and u_form.is_valid():
			p_form.save()
			u_form.save()
			return redirect('staff-profile')
	else:
		p_form = StaffProfileUpdateForm(instance=request.user.staffprofile)
		u_form = StaffUserUpdateForm(instance=request.user)
	return render(request, 'staff/profile_update.html', {'p_form':p_form, 'u_form':u_form})

@login_required
def view_student_bills(request):
	form = CalculateBill(request.GET)

	if form.is_valid():
		search_query = form.cleaned_data['search_query']
		print(search_query)
		try:
			student = StudentProfile.objects.get(bits_id=search_query).user
			student_profile = StudentProfile.objects.get(bits_id=search_query)
			student_bill = StudentBill.objects.get(student=student)

			bill_dict={'Student_BITS_ID': student_profile.bits_id,
					'Breakfast':student_bill.breakfast,
					'Lunch':student_bill.lunch,
					'Dinner':student_bill.dinner,
					'Breakfast_Total': (student_bill.breakfast)*80,
					'Lunch_Total': (student_bill.lunch)*180,
					'Dinner_Total': (student_bill.dinner)*150,
					'Total': (student_bill.breakfast)*80+(student_bill.lunch)*180+(student_bill.dinner)*150}
		except:
			bill_dict=None

	context = {'form': form, 'bill_dict': bill_dict}
	return render(request, 'staff/student_bills.html', context)

def export_bill_to_excel(request):

	temp_csv_file_path = os.path.join(settings.MEDIA_ROOT, 'student_bill.csv')
	student_bill_excel = os.path.join(settings.MEDIA_ROOT, 'student_bill.xlsx')
	with open(temp_csv_file_path, 'w', newline="") as file:
		writer=csv.writer(file)
		for bill in StudentBill.objects.all():
			writer.writerow(['Student BITS ID', bill.student.studentprofile.bits_id])
			writer.writerow(['Breakfast Total', f'{bill.breakfast} * 80 = {bill.breakfast*80}'])
			writer.writerow(['Lunch Total', f'{bill.lunch} * 180 = {bill.lunch*180}'])
			writer.writerow(['Dinner Total', f'{bill.dinner} * 150 = {bill.dinner*150}'])
			writer.writerow(['Total', (bill.breakfast*80)+(bill.lunch*180)+(bill.dinner*150)])
			writer.writerow(['', ''])

	df=pd.read_csv(temp_csv_file_path)
	df.to_excel(student_bill_excel, index=False)

	with open(student_bill_excel, 'rb') as student_bill_excel:
		response = HttpResponse(student_bill_excel.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = f'attachment; filename=student_bill_{str(timezone.now().astimezone(timezone.get_current_timezone()).date())}.xlsx'

	return response


class MenuItemListView(ListView):
	model=MenuItems
	context_object_name='items'
	template_name='staff/menuitems_list.html'
	form_class=ItemsSortForm

	def get_queryset(self):
		queryset = super().get_queryset()
		sortby = self.request.GET.get('sortby')

		if sortby:
			return queryset.order_by(sortby)

		else:
			return queryset.order_by('-avg_rating')
	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sort_form'] = self.form_class(initial={'sortby': self.request.GET.get('sortby')})
		return context


class ComplaintListView(ListView):
	model=Complaint
	template_name = 'staff/complaint_list.html'
	context_object_name = 'complaints'

	ordering=["-date_posted"] 


class UploadMenuView(CreateView):
    model = MessMenu
    fields = ['excel_file']
    success_url = '/staff/'
