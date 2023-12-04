from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import StudentProfileUpdateForm, MarkAttendance, RateMenuItem
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, timedelta
from .models import Complaint, MenuItems, StudentAttendance, StudentBill
from staff.models import MessMenu
from django.utils import timezone
from urllib.parse import unquote
import pandas as pd
import openpyxl
from django.conf import settings
import os



def student_dashboard(request):
    breakfast_start_time=time(7,0)
    breakfast_end_time=time(9,0)
    lunch_start_time=time(12,0)
    lunch_end_time=time(14,0)
    dinner_start_time=time(19,0)
    dinner_end_time=time(21,0)
    today=str(timezone.now().astimezone(timezone.get_current_timezone()).date())
    tomorrow=str((timezone.now().astimezone(timezone.get_current_timezone())+timedelta(days=1)).date())
    current_time=timezone.now().astimezone(timezone.get_current_timezone()).time()


    def time_in_range(current_time,start_time,end_time):
        if start_time <= end_time:
            return start_time < current_time <= end_time
        else:
            return start_time < current_time or current_time <= end_time

    if time_in_range(current_time,breakfast_start_time,breakfast_end_time):
        next_meal="LUNCH"
        current_meal="BREAKFAST"
    elif time_in_range(current_time,breakfast_end_time,lunch_start_time):
        next_meal="LUNCH"
        current_meal=""
    elif time_in_range(current_time,lunch_start_time,lunch_end_time):
        next_meal="DINNER"
        current_meal="LUNCH"
    elif time_in_range(current_time,lunch_end_time,dinner_start_time):
        next_meal="DINNER"
        current_meal=""
    elif time_in_range(current_time,dinner_start_time,dinner_end_time):
        next_meal="BREAKFAST"
        current_meal="DINNER"
    elif time_in_range(current_time,dinner_end_time,breakfast_start_time):
        next_meal="BREAKFAST"
        current_meal=""

    if next_meal=="BREAKFAST" and current_meal=="":
        next_meal_menu=[item.item_name for item in MenuItems.objects.filter(date_to_be_served=tomorrow, meal=next_meal)]
        next_meal_display=f"{tomorrow}'s BREAKFAST"
        current_meal_display=""

    elif next_meal=="BREAKFAST" and current_meal=="DINNER":
        next_meal_menu=[item.item_name for item in MenuItems.objects.filter(date_to_be_served=tomorrow, meal=next_meal)]
        next_meal_display=f"{tomorrow}'s BREAKFAST"
        current_meal_display=f"{today}'s DINNER"
    
    else:
        next_meal_menu=[item.item_name for item in MenuItems.objects.filter(date_to_be_served=today, meal=next_meal)]
        next_meal_display=f"{today}'s {next_meal}"
        if current_meal=="":
            current_meal_display=""
        else:
            current_meal_display=f"{today}'s {current_meal}"
    

    if current_meal!="":
        current_meal_menu=[item.item_name for item in MenuItems.objects.filter(date_to_be_served=today, meal=current_meal)]
    else:
        current_meal_menu=False

    display_attendance_disabled=False
    
    if current_meal=="":
        display_attendance_disabled=True


    most_recent_menu = MessMenu.objects.all().last()
    menu_file_path = most_recent_menu.excel_file.url

    return render(request, 'student/dashboard.html', {'next_meal':next_meal_display,
                                                    'current_meal':current_meal_display,
                                                    'next_meal_menu':next_meal_menu,
                                                    'current_meal_menu':current_meal_menu,
                                                    'disabled_attendance':display_attendance_disabled,
                                                    'menu_file_path':menu_file_path})



class CustomLogoutView(LogoutView):

    def get_success_url(self):
        # Get the 'next' parameter from the URL or use a default redirect URL
        redirect_url = self.request.GET.get('next', 'http://localhost:8000/student')
        return redirect_url



@login_required
def profile(request):
    return render(request, 'student/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=request.user.studentprofile)
        if form.is_valid():
            form.save()
            return redirect('student-profile')
    else:
        form = StudentProfileUpdateForm(request.POST, instance=request.user.studentprofile)
    return render(request, 'student/profile_update.html', {'form': form})

@login_required 
def mark_attendance(request):
    breakfast_start_time=time(7,0)
    breakfast_end_time=time(9,0)
    lunch_start_time=time(12,0)
    lunch_end_time=time(14,0)
    dinner_start_time=time(19,0)
    dinner_end_time=time(21,0)
    today=str(timezone.now().astimezone(timezone.get_current_timezone()).date())
    tomorrow=str((timezone.now().astimezone(timezone.get_current_timezone())+timedelta(days=1)).date())
    current_time=timezone.now().astimezone(timezone.get_current_timezone()).time()

    def time_in_range(current_time,start_time,end_time):
        if start_time <= end_time:
            return start_time < current_time <= end_time
        else:
            return start_time < current_time or current_time <= end_time
    current_meal=""
    if time_in_range(current_time,breakfast_start_time,breakfast_end_time):
        current_meal="BREAKFAST"
    elif time_in_range(current_time,lunch_start_time,lunch_end_time):
        current_meal="LUNCH"
    elif time_in_range(current_time,dinner_start_time,dinner_end_time):
        current_meal="DINNER"

    current_user=request.user
    if request.method == 'POST' and current_meal!="":
        form = MarkAttendance(request.POST,
                                instance=StudentAttendance.objects.get(student=current_user,date=today,meal=current_meal))
        if form.is_valid():
            form.save()
            current_user.studentbill.save()
            return redirect('student-dashboard')
    elif current_meal!="":
        form = MarkAttendance(request.POST, 
                                instance=StudentAttendance.objects.get(student=current_user,date=today,meal=current_meal))
    else:
        form="Attendance cannot be accessed at the moment as there is no ongoing meal"
    
    if current_meal=="":
        attendance=False
    else:
        attendance=StudentAttendance.objects.get(student=request.user,date=today,meal=current_meal).attendance_mark
    if attendance:
        attendance_already_marked=True
    else:
        attendance_already_marked=False
    
    return render(request, 'student/mark_attendance.html', {'form': form, 
                                                            'attendance_already_marked':attendance_already_marked,
                                                            'meal':current_meal,
                                                            'date':today})





#Complaint Views
class ComplaintListView(ListView):
    model=Complaint
    template_name = 'student/complaint_list.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        return Complaint.objects.filter(student=self.request.user.studentprofile)[::-1]

class ComplaintDetailView(DetailView):
    model=Complaint
    context_object_name = 'complaint'

class ComplaintCreateView(CreateView):
    model = Complaint
    fields = ['title', 'complaint', 'image']

    def form_valid(self,form):
        form.instance.student = self.request.user.studentprofile
        return super().form_valid(form)

class ComplaintUpdateView(UpdateView):
    model = Complaint
    fields = ['title', 'complaint', 'image']
    success_url='/student/complaints'

    def form_valid(self, form):
        form.instance.student = self.request.user.studentprofile
        return super().form_valid(form)

class ComplaintDeleteView(DeleteView):
    model=Complaint
    success_url='/student/complaints'





def meals_attended(request):
    attended=StudentAttendance.objects.filter(student=request.user, attendance_mark=True)[::-1][:5]
    if len(attended)>0:
        meals_attended_items={}
        for attendance in attended:
            meals_attended_items[f"{attendance.date}'s {attendance.meal}"]=[item.item_name for item in MenuItems.objects.filter(date_to_be_served=attendance.date, meal=attendance.meal)]

    else:
        attended=None
    print(meals_attended_items)

    return render(request, 'student/meals_attended.html', {'meals_attended_items':meals_attended_items, 'attended':attended})


def rate_an_item(request, item_tag):
    space_positions=[]
    for index,char in enumerate(item_tag):
        if char==" ":
            space_positions.append(index)

    date_part = item_tag[:(space_positions[0])]
    meal_part = item_tag[space_positions[0] + 1:space_positions[1]]
    item_name_part = item_tag[space_positions[1] + 1:]

    instance = MenuItems.objects.get(
        date_to_be_served=date_part,
        meal=meal_part,
        item_name=item_name_part
    )

    if request.method == 'POST':
        form = RateMenuItem(request.POST)
        if form.is_valid():
            instance.ratings += form.cleaned_data['add_rating']
            instance.save()
            return redirect('meals-attended')  # Redirect to a success page or another view
    else:
        form = RateMenuItem(request.POST)

    return render(request, 'student/rate_menu_item.html', {'form': form})


def display_current_mess_menu(request):
    menu_file = MessMenu.objects.all().last()

    # Serve the Excel file
    response = FileResponse(menu_file.excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'inline; filename="{menu_file.excel_file.name}"'
    return response