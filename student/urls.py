from django.urls import path, include
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path("", views.student_dashboard , name="student-dashboard"),
    path('accounts/', include('allauth.urls'),),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('logout', views.CustomLogoutView.as_view(), name='student-logout'),
    path('profile/', views.profile , name='student-profile'),
    path('profile/update/', views.profile_update , name='student-profile-update'),
    path('complaints/', views.ComplaintListView.as_view() , name='student-complaints'),
    path('complaints/<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint-detail'),
    path('complaints/write/', views.ComplaintCreateView.as_view(), name='complaint-create'),
    path('complaints/<int:pk>/update/', views.ComplaintUpdateView.as_view(), name='complaint-update'),
    path('complaints/<int:pk>/delete/', views.ComplaintDeleteView.as_view(), name='complaint-delete'),
    path('mark-attendance/', views.mark_attendance, name='student-mark-attendance'),
    path('meals-attended/', views.meals_attended, name='meals-attended'),
    path('meals-attended/rate-an-item/<path:item_tag>/', views.rate_an_item, name='rate-an-item'),
    path("current-mess-menu/", views.display_current_mess_menu, name='current-mess-menu')
]