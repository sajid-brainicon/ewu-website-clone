from django.shortcuts import render, get_object_or_404
from .models import Slider, Notice, News, Event, ImportantDate
import datetime

# Create your views here.

def home(request):
    sliders = Slider.objects.all()
    notices = Notice.objects.all()[:5]
    news_list = News.objects.all()[:3]
    events = Event.objects.filter(is_active=True)[:5]
    important_dates = ImportantDate.objects.filter(date__gte=datetime.date.today())[:5]
    return render(request, 'home.html', {
        'sliders': sliders,
        'notices': notices,
        'news_list': news_list,
    })

def about(request):
    return render(request, 'about.html')

def admissions(request):
    return render(request, 'admissions.html')

def departments(request):
    departments_list = [
        {'name': 'Computer Science & Engineering', 'icon': 'fa-laptop-code', 'desc': 'Cutting-edge curriculum with AI, ML, and software engineering.'},
        {'name': 'Electrical & Electronic Engineering', 'icon': 'fa-bolt', 'desc': 'Power systems, electronics, and telecommunications.'},
        {'name': 'Business Administration', 'icon': 'fa-chart-line', 'desc': 'Management, finance, marketing, and entrepreneurship.'},
        {'name': 'Pharmacy', 'icon': 'fa-capsules', 'desc': 'Pharmaceutical sciences and clinical research.'},
        {'name': 'Economics', 'icon': 'fa-coins', 'desc': 'Microeconomics, macroeconomics, and econometrics.'},
        {'name': 'English', 'icon': 'fa-book-open', 'desc': 'Language, literature, and linguistics.'},
        {'name': 'Law', 'icon': 'fa-gavel', 'desc': 'Legal studies and justice administration.'},
        {'name': 'Architecture', 'icon': 'fa-drafting-compass', 'desc': 'Design, planning, and sustainable architecture.'},
    ]
    return render(request, 'departments.html', {'departments': departments_list})

def faculty(request):
    faculty_members = [
        {'name': 'Dr. Ahmed Hossain', 'designation': 'Professor, CSE', 'image': 'images/placeholder.jpg'},
        {'name': 'Prof. Nusrat Jahan', 'designation': 'Chairperson, EEE', 'image': 'images/placeholder.jpg'},
        {'name': 'Dr. Kamal Uddin', 'designation': 'Associate Professor, BBA', 'image': 'images/placeholder.jpg'},
        {'name': 'Dr. Farhana Rahman', 'designation': 'Professor, Pharmacy', 'image': 'images/placeholder.jpg'},
        {'name': 'Md. Rafiqul Islam', 'designation': 'Lecturer, Economics', 'image': 'images/placeholder.jpg'},
        {'name': 'Prof. Sharmin Akhter', 'designation': 'Dean, Arts & Humanities', 'image': 'images/placeholder.jpg'},
    ]
    return render(request, 'faculty.html', {'faculty': faculty_members})

def programs(request):
    return render(request, 'programs.html')

def research(request):
    return render(request, 'research.html')

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notices.html', {'notices': notices})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notice_details.html', {'notice': notice})

def news_list(request):
    all_news = News.objects.all()
    return render(request, 'news.html', {'all_news': all_news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news_details.html', {'news': news_item})

def contact(request):
    return render(request, 'contact.html')

def gallery(request):
    # Static image list (replace with real images)
    gallery_images = [
        'images/placeholder.jpg',
        'images/placeholder.jpg',
        'images/placeholder.jpg',
        'images/placeholder.jpg',
        'images/placeholder.jpg',
        'images/placeholder.jpg',
    ]
    return render(request, 'gallery.html', {'gallery_images': gallery_images})