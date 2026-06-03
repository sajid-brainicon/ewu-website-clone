from django.urls import path
from . import views

urlpatterns = [
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
    path('chat/', views.chat_view, name='chat'),
    path('chat/',               views.chat_view,     name='chat'),
]