from django.urls import path
from .views import *

urlpatterns = [
    #admin
    path('login/', admin_login, name='login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout', admin_logout, name="logout"),
    path('alumni/', alumni, name="alumni"),
    path('alumni_list/', alumni_list, name="alumni_list"),
    path('alumni_create/', alumni_create, name="alumni_create"),
    path('alumni_update/<int:pk>/', alumni_update, name="alumni_update"),
    path('alumni_delete/<int:pk>/', alumni_delete, name="alumni_delete"),
    path('alumni_upload/', alumni_upload, name="alumni_upload"),
    path('export_pdf_alumni/', export_pdf_alumni, name="export_pdf_alumni"),
    path('export_pdf_participants', export_pdf_participants, name="export_pdf_participants"),
    path('participants_list/', participants_list, name="participants_list"),
    
    #alumni
    path('', alumni_home, name='alumni_home'),
    path('alumni_create_by_user/', alumni_create_by_user, name="alumni_create_by_user"),
    path('alumni_camp/', alumni_camp, name="alumni_camp"),
    path('camp_registration/', camp_registration, name="camp_registration"),
]
