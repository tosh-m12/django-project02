from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/<int:employee_id>/', views.employee_edit, name='employee_edit'),
    path('employees/', views.employee_list, name='employee_list'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('download_csv/', views.download_csv, name='download_csv'),   
]
