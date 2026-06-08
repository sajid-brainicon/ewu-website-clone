import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import StudentProfile
from main.models import Notice, News, Event, Job


EWU_STUDENT_DOMAIN = 'std.ewubd.edu'

DEPT_CHOICES = [
    ('CSE', 'Computer Science & Engineering'),
    ('EEE', 'Electrical & Electronic Engineering'),
    ('BBA', 'Business Administration'),
    ('Pharmacy', 'Pharmacy'),
    ('Economics', 'Economics'),
    ('English', 'English'),
    ('Law', 'Law'),
    ('Architecture', 'Architecture'),
    ('Admin', 'Administration'),
]


def _is_student(user):
    return (
        user.is_authenticated and
        user.email and
        user.email.endswith(f'@{EWU_STUDENT_DOMAIN}') and
        hasattr(user, 'student_profile')
    )


def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not _is_student(request.user):
            messages.error(request, 'Access denied. Please login with a valid student account.')
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def student_register(request):
    if request.user.is_authenticated and _is_student(request.user):
        return redirect('student_dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        student_id = request.POST.get('student_id', '').strip()
        program = request.POST.get('program', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not email.endswith(f'@{EWU_STUDENT_DOMAIN}'):
            messages.error(request, f'Only @{EWU_STUDENT_DOMAIN} emails are allowed.')
            return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})

        if StudentProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already registered.')
            return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})

        try:
            username = email.split('@')[0]
            base = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{counter}'
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                program=program,
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('student_login')

        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            print(e)

    return render(request, 'student/register.html', {
        'programs': StudentProfile.PROGRAM_CHOICES,
    })


def student_login(request):
    if request.user.is_authenticated and _is_student(request.user):
        return redirect('student_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email.endswith(f'@{EWU_STUDENT_DOMAIN}'):
            messages.error(request, f'Only @{EWU_STUDENT_DOMAIN} emails can login here.')
            return render(request, 'student/login.html')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user and _is_student(user):
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'student/login.html')


def student_logout(request):
    logout(request)
    return redirect('student_login')


@student_login_required
def student_dashboard(request):
    profile = request.user.student_profile
    today = datetime.date.today()
    
    context = {
        'title': 'Student Dashboard',
        'profile': profile,
        'recent_notices': Notice.objects.order_by('-created_at')[:5],
        'recent_news': News.objects.order_by('-created_at')[:4],
        'upcoming_events': Event.objects.filter(is_active=True, date__gte=today).order_by('date')[:4],
        'active_jobs': Job.objects.filter(is_active=True).order_by('-posted_at')[:4],
    }
    return render(request, 'student/dashboard.html', context)

@student_login_required
def student_notices(request):
    q = request.GET.get('q', '').strip()
    notices = Notice.objects.order_by('-created_at')
    if q:
        notices = notices.filter(title__icontains=q)
    return render(request, 'student/notices.html', {
        'notices': notices,
        'q': q,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'student/notice_detail.html', {
        'notice': notice,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_news(request):
    q = request.GET.get('q', '').strip()
    news_list = News.objects.order_by('-created_at')
    if q:
        news_list = news_list.filter(title__icontains=q)
    return render(request, 'student/news.html', {
        'news_list': news_list,
        'q': q,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'student/news_detail.html', {
        'news': news,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_events(request):
    today = datetime.date.today()
    events = Event.objects.filter(is_active=True, date__gte=today).order_by('date')
    return render(request, 'student/events.html', {
        'events': events,
        'profile': request.user.student_profile,
    })

@student_login_required
def student_event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    return render(request, 'student/event_detail.html', {
        'event': event,
        'profile': request.user.student_profile,
    })

@student_login_required
def student_jobs(request):
    q = request.GET.get('q', '').strip()
    dept = request.GET.get('dept', '')
    jobs = Job.objects.filter(is_active=True).order_by('-posted_at')
    
    if q:
        jobs = jobs.filter(title__icontains=q)
    if dept:
        jobs = jobs.filter(department=dept)
        
    return render(request, 'student/jobs.html', {
        'jobs': jobs,
        'q': q,
        'dept': dept,
        'dept_choices': DEPT_CHOICES,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, 'student/job_detail.html', {
        'job': job,
        'profile': request.user.student_profile,
    })


@student_login_required
def student_profile(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.save()

        profile.phone = request.POST.get('phone', '').strip()
        profile.address = request.POST.get('address', '').strip()
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('student_profile')

    return render(request, 'student/profile.html', {'profile': profile})


@student_login_required
def student_change_password(request):
    if request.method == 'POST':
        current = request.POST.get('current_password', '')
        new_pw = request.POST.get('new_password', '')
        confirm = request.POST.get('confirm_password', '')

        if not request.user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new_pw != confirm:
            messages.error(request, 'New passwords do not match.')
        elif len(new_pw) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new_pw)
            request.user.save()
            user = authenticate(username=request.user.username, password=new_pw)
            if user:
                login(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('student_profile')

    return render(request, 'student/change_password.html', {'profile': request.user.student_profile})