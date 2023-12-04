from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from staff.signals import mess_menu_uploaded
from allauth.socialaccount.models import SocialAccount
from .models import StudentProfile, MenuItems, StudentAttendance, StudentBill
from staff.models import StaffProfile
from django.conf import settings
import os 

@receiver(user_logged_in)
def create_user_profile(sender, request, user, **kwargs):
    StudentProfile.objects.get_or_create(user=user, google_account=SocialAccount.objects.get(user=user))
    user.studentprofile.save()
    StudentBill.objects.get_or_create(student = user)
    user.studentbill.save()


@receiver(user_logged_in)
def create_student_attendance(sender, request, user, **kwargs):
    instance, created = StudentAttendance.objects.filter_or_create(student=user)

@receiver(mess_menu_uploaded)
def new_mess_menu_uploaded(sender, instance, **kwargs):
    import pandas as pd
    import json

    menu_file=instance.excel_file
    #Reading the excel file, data cleaning
    df=pd.read_excel(f'./{menu_file.url}')
        
    #Converting datetime objects column to string (Indexing of "data" was getting long and annoying)
    for i in df.columns:
        df[i][0] = df[i][0].strftime("%Y-%m-%d")
        
    #Creating a dictionary with each date as a key and another dictionary as a value
    data={}
    for i in df.loc[0]: 
        data[i]={'BREAKFAST':[], 'LUNCH':[], 'DINNER':[]} 
        

    #Finding range of indices of food item cells using filter
    row=df.columns[0]
    filt1= (df[row]=='BREAKFAST')
    j=[i for i in df.loc[filt1,row].index]
    s1=j[0]+1
    filt2= (df[row]=='LUNCH')
    k=[i for i in df.loc[filt2,row].index]
    e1=k[0]-2
    s2=k[0]+1
    filt3= (df[row]=='DINNER')
    l=[i for i in df.loc[filt3,row].index]
    e2=l[0]-2
    s3=l[0]+1



    #Serialization of data in the form of a Python dictionary
    #I know it looks shabby but that's because I used list comprehension and excluding the unwanted data was a little hard. 
    df.fillna(" ", inplace=True) #To replace NaN with a space so its easier to remove
    for i in df.columns:
        data[df.loc[0,i]]['BREAKFAST']=[item for item in df.loc[s1:e1,i] if item[0].isalpha()]
        data[df.loc[0,i]]['LUNCH']=[item for item in df.loc[s2:e2,i] if item[0].isalpha()]
        data[df.loc[0,i]]['DINNER']=[item for item in df.loc[s3:,i] if item[0].isalpha()]


    file_path=os.path.join(settings.MEDIA_ROOT, 'mess_menu.json')

    #Writing to data to new JSON file
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)

    with open(file_path,'r') as file:
        date_wise_menu_dict=json.load(file)

    for date in date_wise_menu_dict:
        for meal in date_wise_menu_dict[date]:
            for item in date_wise_menu_dict[date][meal]:
                MenuItems.objects.get_or_create(date_to_be_served=date, meal=meal, item_name=item)

    for profile in StudentProfile.objects.all():
        for date in date_wise_menu_dict:
            for meal in date_wise_menu_dict[date]:
                StudentAttendance.objects.get_or_create(student=profile.user, 
                                                        date=date,
                                                        meal=meal)
    

