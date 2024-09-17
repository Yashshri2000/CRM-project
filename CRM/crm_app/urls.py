from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name="home"),
    path('user-login', user_login, name="user_login"),
    path('user-home', user_home, name="user_home"),
    path('signup', signup, name="signup"),
    path('jobs', all_jobs, name="jobs"),
    path('job-detail/<int:id>/', job_detail, name="job_detail"),
    path('job-apply/<int:id>/', job_apply, name="job_apply"),
    path('user-dashboard', user_dashboard, name="user_dashboard"),
]