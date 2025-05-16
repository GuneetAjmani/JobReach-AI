from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('search/', views.search_jobs, name='search_jobs'),
    path('jobs/<str:job_id>/generate-cold-mail/', views.generate_cold_mail, name='generate_cold_mail'),
] 