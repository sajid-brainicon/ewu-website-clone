from django.urls import path
from . import views

urlpatterns = [
    # ====================== PUBLIC PAGES ======================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('departments/', views.departments, name='departments'),
    path('faculty/', views.faculty, name='faculty'),
    path('programs/', views.programs, name='programs'),
    path('research/', views.research, name='research'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('chat/', views.chat_view, name='chat'),

    # ====================== ADMIN ======================
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Notice Management
    path('admin/notices/', views.notice_list_admin, name='admin_notice_list'),
    path('admin/notices/create/', views.notice_create, name='admin_notice_create'),
    path('admin/notices/<int:pk>/edit/', views.notice_edit, name='admin_notice_edit'),
    path('admin/notices/<int:pk>/delete/', views.notice_delete, name='admin_notice_delete'),

    # News Management
    path('admin/news/', views.news_list_admin, name='admin_news_list'),
    path('admin/news/create/', views.news_create, name='admin_news_create'),
    path('admin/news/<int:pk>/edit/', views.news_edit, name='admin_news_edit'),
    path('admin/news/<int:pk>/delete/', views.news_delete, name='admin_news_delete'),

    # Student Dashboard
    path('student/', views.student_dashboard, name='student_dashboard'),
]