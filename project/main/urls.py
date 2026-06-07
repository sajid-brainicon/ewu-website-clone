from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('admissions/', views.admissions, name='admissions'),
    path('programs/', views.programs, name='programs'),
    path('research/', views.research, name='research'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('faculty/', views.faculty, name='faculty'),
    path('gallery/', views.gallery, name='gallery'),
    
    # Notices
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    
    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Jobs
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    
    # Chat
    path('chat/', views.chat_view, name='chat'),
    
    # Student Dashboard
    path('student/', views.student_dashboard, name='student_dashboard'),

    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    
    # Slider CRUD
    path('admin/sliders/', views.slider_list, name='admin_slider_list'),
    path('admin/sliders/create/', views.slider_create, name='admin_slider_create'),
    path('admin/sliders/<int:pk>/edit/', views.slider_edit, name='admin_slider_edit'),
    path('admin/sliders/<int:pk>/delete/', views.slider_delete, name='admin_slider_delete'),

    # Notice CRUD
    path('admin/notices/', views.notice_list_admin, name='admin_notice_list'),
    path('admin/notices/create/', views.notice_create, name='admin_notice_create'),
    path('admin/notices/<int:pk>/edit/', views.notice_edit, name='admin_notice_edit'),
    path('admin/notices/<int:pk>/delete/', views.notice_delete, name='admin_notice_delete'),

    # News CRUD
    path('admin/news/', views.news_list_admin, name='admin_news_list'),
    path('admin/news/create/', views.news_create, name='admin_news_create'),
    path('admin/news/<int:pk>/edit/', views.news_edit, name='admin_news_edit'),
    path('admin/news/<int:pk>/delete/', views.news_delete, name='admin_news_delete'),

    # Event CRUD
    path('admin/events/', views.event_list, name='admin_event_list'),
    path('admin/events/create/', views.event_create, name='admin_event_create'),
    path('admin/events/<int:pk>/edit/', views.event_edit, name='admin_event_edit'),
    path('admin/events/<int:pk>/delete/', views.event_delete, name='admin_event_delete'),

    # Important Dates CRUD
    path('admin/dates/', views.date_list, name='admin_date_list'),
    path('admin/dates/create/', views.date_create, name='admin_date_create'),
    path('admin/dates/<int:pk>/edit/', views.date_edit, name='admin_date_edit'),
    path('admin/dates/<int:pk>/delete/', views.date_delete, name='admin_date_delete'),

    # Achievement CRUD
    path('admin/achievements/', views.achievement_list, name='admin_achievement_list'),
    path('admin/achievements/create/', views.achievement_create, name='admin_achievement_create'),
    path('admin/achievements/<int:pk>/edit/', views.achievement_edit, name='admin_achievement_edit'),
    path('admin/achievements/<int:pk>/delete/', views.achievement_delete, name='admin_achievement_delete'),

    # Job CRUD
    path('admin/jobs/', views.job_list_admin, name='admin_job_list'),
    path('admin/jobs/create/', views.job_create, name='admin_job_create'),
    path('admin/jobs/<int:pk>/edit/', views.job_edit, name='admin_job_edit'),
    path('admin/jobs/<int:pk>/delete/', views.job_delete, name='admin_job_delete'),

    # Gallery CRUD
    path('admin/gallery/', views.gallery_list_admin, name='admin_gallery_list'),
    path('admin/gallery/create/', views.gallery_create, name='admin_gallery_create'),
    path('admin/gallery/<int:pk>/edit/', views.gallery_edit, name='admin_gallery_edit'),
    path('admin/gallery/<int:pk>/delete/', views.gallery_delete, name='admin_gallery_delete'),
]