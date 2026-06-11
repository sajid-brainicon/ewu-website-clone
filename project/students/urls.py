from django.urls import path
from . import views

urlpatterns = [
    # Only registration lives here — everything else moved to main/urls.py
    path('register/', views.student_register, name='student_register'),
]