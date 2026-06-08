from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    
    # Notices
    path('notices/', views.student_notices, name='student_notices'),
    path('notices/<int:pk>/', views.student_notice_detail, name='student_notice_detail'),
    
    # News
    path('news/', views.student_news, name='student_news'),
    path('news/<int:pk>/', views.student_news_detail, name='student_news_detail'),
    
    # Events
    path('events/', views.student_events, name='student_events'),
    path('events/<int:pk>/', views.student_event_detail, name='student_event_detail'),
    
    # Jobs
    path('jobs/', views.student_jobs, name='student_jobs'),
    path('jobs/<int:pk>/', views.student_job_detail, name='student_job_detail'),
    
    # Profile
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/password/', views.student_change_password, name='student_change_password'),
    
    # Auth
    path('login/', views.student_login, name='student_login'),
    path('register/', views.student_register, name='student_register'),
    path('logout/', views.student_logout, name='student_logout'),
]