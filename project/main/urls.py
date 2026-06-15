from django.urls import path, include
from . import views
from . import role_views

urlpatterns = [
    path('',             views.home,        name='home'),
    path('about/',       views.about,       name='about'),
    path('admissions/',  views.admissions,  name='admissions'),
    path('programs/',    views.programs,    name='programs'),
    path('research/',    views.research,    name='research'),
    path('contact/',     views.contact,     name='contact'),
    path('departments/', views.departments, name='departments'),
    path('faculty/',     views.faculty,     name='faculty'),
    path('gallery/',     views.gallery,     name='gallery'),
    path('chat/',        views.chat_view,   name='chat'),

    
    path('login/',   views.unified_login,   name='login'),
    path('logout/',  views.unified_logout,  name='logout'),   
    path('dashboard/', views.unified_dashboard, name='dashboard'),    
    path('notices/',          views.unified_notices,      name='student_notices'),
    path('notices/<int:pk>/', views.unified_notice_detail,name='student_notice_detail'),
    path('news/',             views.unified_news,         name='student_news'),
    path('news/<int:pk>/',    views.unified_news_detail,  name='student_news_detail'),
    path('events/',           views.unified_events,       name='student_events'),
    path('events/<int:pk>/',  views.unified_event_detail, name='student_event_detail'),
    path('jobs/',             views.unified_jobs,         name='student_jobs'),
    path('jobs/<int:pk>/',    views.unified_job_detail,   name='student_job_detail'),

    
    path('profile/',          views.unified_profile,         name='student_profile'),
    path('profile/password/', views.unified_change_password, name='student_change_password'),

    path('dashboard/sliders/',                      views.slider_list,        name='admin_slider_list'),
    path('dashboard/sliders/create/',               views.slider_create,      name='admin_slider_create'),
    path('dashboard/sliders/<int:pk>/edit/',        views.slider_edit,        name='admin_slider_edit'),
    path('dashboard/sliders/<int:pk>/delete/',      views.slider_delete,      name='admin_slider_delete'),

    path('dashboard/notices/',                      views.notice_list_admin,  name='admin_notice_list'),
    path('dashboard/notices/create/',               views.notice_create,      name='admin_notice_create'),
    path('dashboard/notices/<int:pk>/edit/',        views.notice_edit,        name='admin_notice_edit'),
    path('dashboard/notices/<int:pk>/delete/',      views.notice_delete,      name='admin_notice_delete'),

    path('dashboard/news/',                         views.news_list_admin,    name='admin_news_list'),
    path('dashboard/news/create/',                  views.news_create,        name='admin_news_create'),
    path('dashboard/news/<int:pk>/edit/',           views.news_edit,          name='admin_news_edit'),
    path('dashboard/news/<int:pk>/delete/',         views.news_delete,        name='admin_news_delete'),

    path('dashboard/events/',                       views.event_list,         name='admin_event_list'),
    path('dashboard/events/create/',                views.event_create,       name='admin_event_create'),
    path('dashboard/events/<int:pk>/edit/',         views.event_edit,         name='admin_event_edit'),
    path('dashboard/events/<int:pk>/delete/',       views.event_delete,       name='admin_event_delete'),

    path('dashboard/dates/',                        views.date_list,          name='admin_date_list'),
    path('dashboard/dates/create/',                 views.date_create,        name='admin_date_create'),
    path('dashboard/dates/<int:pk>/edit/',          views.date_edit,          name='admin_date_edit'),
    path('dashboard/dates/<int:pk>/delete/',        views.date_delete,        name='admin_date_delete'),

    path('dashboard/achievements/',                 views.achievement_list,   name='admin_achievement_list'),
    path('dashboard/achievements/create/',          views.achievement_create, name='admin_achievement_create'),
    path('dashboard/achievements/<int:pk>/edit/',   views.achievement_edit,   name='admin_achievement_edit'),
    path('dashboard/achievements/<int:pk>/delete/', views.achievement_delete, name='admin_achievement_delete'),

    path('dashboard/jobs/',                         views.job_list_admin,     name='admin_job_list'),
    path('dashboard/jobs/create/',                  views.job_create,         name='admin_job_create'),
    path('dashboard/jobs/<int:pk>/edit/',           views.job_edit,           name='admin_job_edit'),
    path('dashboard/jobs/<int:pk>/delete/',         views.job_delete,         name='admin_job_delete'),

    path('dashboard/gallery/',                      views.gallery_list_admin, name='admin_gallery_list'),
    path('dashboard/gallery/create/',               views.gallery_create,     name='admin_gallery_create'),
    path('dashboard/gallery/<int:pk>/edit/',        views.gallery_edit,       name='admin_gallery_edit'),
    path('dashboard/gallery/<int:pk>/delete/',      views.gallery_delete,     name='admin_gallery_delete'),

    path('dashboard/roles/',                  role_views.role_list,         name='role_list'),
    path('dashboard/roles/create/',           role_views.role_create,       name='role_create'),
    path('dashboard/roles/<int:pk>/edit/',    role_views.role_edit,         name='role_edit'),
    path('dashboard/roles/<int:pk>/delete/',  role_views.role_delete,       name='role_delete'),
    path('dashboard/users/',                  role_views.user_list,         name='rbac_user_list'),
    path('dashboard/users/<int:pk>/roles/',   role_views.user_role_assign,  name='user_role_assign'),
]