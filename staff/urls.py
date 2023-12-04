from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard , name="staff-dashboard"),
    path("register/", views.register, name="staff-register"),
    path("login/", views.CustomLoginView.as_view(template_name='staff/login.html'), name="staff-login"),
    path("logout", views.CustomLogoutView.as_view(), name="staff-logout"),
    path("profile/", views.profile, name="staff-profile"),
    path("profile/update/", views.profile_update, name="staff-profile-update"),
    path("complaints/", views.ComplaintListView.as_view(), name='staff-view-complaints'),
    path("upload-mess-menu/", views.UploadMenuView.as_view(), name='staff-upload-menu'),
    path("student-bills/", views.view_student_bills, name='staff-view-student-bills'),
    path("student-bill/export/", views.export_bill_to_excel, name='export-student-bill'),
    path("menu-item-ratings/", views.MenuItemListView.as_view(), name='menu-item-ratings'),
]

