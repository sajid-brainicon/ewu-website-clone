import datetime
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import (
    Slider, Notice, News, Event, ImportantDate,
    ChatMessage, Achievement, Job
)


# ====================== PUBLIC PAGES ======================
def home(request):
    sliders = Slider.objects.all()
    notices = Notice.objects.all()[:5]
    news_list = News.objects.all()[:4]
    events = Event.objects.filter(is_active=True).order_by('date')[:5]
    important_dates = ImportantDate.objects.filter(
        date__gte=datetime.date.today(), is_active=True
    ).order_by('date')[:5]
    achievements = Achievement.objects.filter(is_active=True)

    return render(request, 'home.html', {
        'sliders': sliders,
        'notices': notices,
        'news_list': news_list,
        'events': events,
        'important_dates': important_dates,
        'achievements': achievements,
    })


def about(request):
    return render(request, 'about.html')


def admissions(request):
    return render(request, 'admissions.html')


def programs(request):
    return render(request, 'programs.html')


def research(request):
    return render(request, 'research.html')


def contact(request):
    return render(request, 'contact.html')


def departments(request):
    departments_list = [
        {'name': 'Computer Science & Engineering', 'icon': 'fa-laptop-code', 'desc': 'AI, ML, software engineering and more.'},
        {'name': 'Electrical & Electronic Engineering', 'icon': 'fa-bolt', 'desc': 'Power systems, electronics, and telecom.'},
        {'name': 'Business Administration', 'icon': 'fa-chart-line', 'desc': 'Management, finance, marketing.'},
        {'name': 'Pharmacy', 'icon': 'fa-capsules', 'desc': 'Pharmaceutical sciences and clinical research.'},
        {'name': 'Economics', 'icon': 'fa-coins', 'desc': 'Micro/macro economics and econometrics.'},
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


def gallery(request):
    return render(request, 'gallery.html')


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


def jobs(request):
    return render(request, 'jobs.html')


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_details.html', {'job': job})


# ====================== CHAT VIEW ======================
@csrf_exempt
def chat_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"reply": "Please type a message."})

        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        ChatMessage.objects.create(
            session_key=session_key,
            sender="user",
            message=user_message
        )

        context = ""
        try:
            from .rag import get_relevant_context
            context = get_relevant_context(user_message)
        except:
            pass

        history = list(ChatMessage.objects.filter(
            session_key=session_key
        ).order_by('-created_at')[:6])[::-1]

        history_text = ""
        for h in history[:-1]:
            role = "User" if h.sender == "user" else "Assistant"
            history_text += f"{role}: {h.message}\n"

        if context:
            prompt = f"""You are the official AI Assistant for East West University (EWU).
Answer ONLY using the provided context. Be helpful and concise.

CONTEXT:
{context}

HISTORY:
{history_text}
User: {user_message}
Assistant:"""
        else:
            prompt = f"""You are the official AI Assistant for East West University (EWU), Bangladesh.
Be helpful and polite.

HISTORY:
{history_text}
User: {user_message}
Assistant:"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 500}
            },
            timeout=90
        )

        if response.status_code == 200:
            reply = response.json().get("response", "").strip()
        else:
            reply = "Sorry, the AI is not responding right now."

        ChatMessage.objects.create(
            session_key=session_key,
            sender="bot",
            message=reply
        )

        return JsonResponse({"reply": reply})

    except Exception as e:
        print(f"Chat Error: {e}")
        return JsonResponse({
            "reply": "Sorry, I'm having trouble right now. Please call 09666775577."
        })


# ====================== ADMIN VIEWS ======================
def admin_login(request):
    """Always show login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin/admin_login.html')   # ← Fixed path


@login_required(login_url='/admin/login/')
def admin_dashboard(request):
    total_notices = Notice.objects.count()
    total_news = News.objects.count()
    recent_notices = Notice.objects.all().order_by('-created_at')[:5]
    recent_news = News.objects.all().order_by('-created_at')[:5]

    context = {
        'total_notices': total_notices,
        'total_news': total_news,
        'recent_notices': recent_notices,
        'recent_news': recent_news,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin_login')


# ====================== NOTICE CRUD ======================
@login_required
def notice_list_admin(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'admin/notice_list.html', {'notices': notices})


@login_required
def notice_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Notice.objects.create(title=title, content=content)
        messages.success(request, 'Notice created successfully!')
        return redirect('admin_notice_list')
    return render(request, 'admin/notice_form.html')


@login_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.content = request.POST.get('content')
        notice.save()
        messages.success(request, 'Notice updated successfully!')
        return redirect('admin_notice_list')
    return render(request, 'admin/notice_form.html', {'notice': notice, 'edit': True})


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.success(request, 'Notice deleted successfully!')
    return redirect('admin_notice_list')


# ====================== NEWS CRUD ======================
@login_required
def news_list_admin(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'admin/news_list.html', {'news_list': news_list})


@login_required
def news_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        News.objects.create(title=title, content=content)
        messages.success(request, 'News created successfully!')
        return redirect('admin_news_list')
    return render(request, 'admin/news_form.html')


@login_required
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        messages.success(request, 'News updated successfully!')
        return redirect('admin_news_list')
    return render(request, 'admin/news_form.html', {'news': news, 'edit': True})


@login_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    messages.success(request, 'News deleted successfully!')
    return redirect('admin_news_list')


# Student Dashboard
def student_dashboard(request):
    return render(request, 'student/dashboard.html', {'title': 'Student Dashboard'})