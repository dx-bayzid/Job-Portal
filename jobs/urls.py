from django.urls import path
from . import views

urlpatterns = [
    path('post_job/', views.post_job, name = 'post_job'),
    path('job_details/<int:job_id>', views.job_details, name = 'job_details'),
    path('job_list/', views.job_list, name = 'job_list'),
]