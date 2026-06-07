import datetime
import json
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Slider, Notice, News, Event, ImportantDate,
    ChatMessage, Achievement, Job, GalleryCategory, GalleryPhoto
)


# ====================== HELPERS ======================
def _is_staff(user):
    return user.is_authenticated and user.is_staff


def _staff_required(view_func):
    return login_required(login_url='/admin/login/')(
        user_passes_test(_is_staff, login_url='/admin/login/')(view_func)
    )


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


def home(request):
    return render(request, 'home.html', {
        'sliders': Slider.objects.all(),
        'notices': Notice.objects.all()[:5],
        'news_list': News.objects.all()[:4],
        'events': Event.objects.filter(is_active=True).order_by('date')[:5],
        'important_dates': ImportantDate.objects.filter(
            date__gte=datetime.date.today(), is_active=True
        ).order_by('date')[:5],
        'achievements': Achievement.objects.filter(is_active=True),
    })


def about(request):       return render(request, 'about.html')
def admissions(request):  return render(request, 'admissions.html')
def programs(request):    return render(request, 'programs.html')
def research(request):    return render(request, 'research.html')
def contact(request):     return render(request, 'contact.html')


def departments(request):
    departments_list = [
        {'name': 'Computer Science & Engineering', 'icon': 'fa-laptop-code', 'desc': 'AI, ML, software engineering.'},
        {'name': 'Electrical & Electronic Engineering', 'icon': 'fa-bolt', 'desc': 'Power systems, electronics, telecom.'},
        {'name': 'Business Administration', 'icon': 'fa-chart-line', 'desc': 'Management, finance, marketing.'},
        {'name': 'Pharmacy', 'icon': 'fa-capsules', 'desc': 'Pharmaceutical sciences.'},
        {'name': 'Economics', 'icon': 'fa-coins', 'desc': 'Micro/macro economics.'},
        {'name': 'English', 'icon': 'fa-book-open', 'desc': 'Language, literature, linguistics.'},
        {'name': 'Law', 'icon': 'fa-gavel', 'desc': 'Legal studies.'},
        {'name': 'Architecture', 'icon': 'fa-drafting-compass', 'desc': 'Design, planning, architecture.'},
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
    cats = GalleryCategory.objects.prefetch_related('photos').all()
    sel = request.GET.get('cat')
    photos = GalleryPhoto.objects.filter(is_active=True, category__id=sel) if sel else GalleryPhoto.objects.filter(is_active=True)
    return render(request, 'gallery.html', {
        'photos': photos,
        'categories': cats,
        'selected_cat': sel
    })


def notice_list(request):
    return render(request, 'notices.html', {'notices': Notice.objects.all()})


def notice_detail(request, pk):
    return render(request, 'notice_details.html', {'notice': get_object_or_404(Notice, pk=pk)})


def news_list(request):
    return render(request, 'news.html', {'all_news': News.objects.all()})


def news_detail(request, pk):
    return render(request, 'news_details.html', {'news': get_object_or_404(News, pk=pk)})


def jobs(request):
    dept = request.GET.get('dept')
    all_jobs = Job.objects.filter(is_active=True).order_by('-id')
    if dept:
        all_jobs = all_jobs.filter(department=dept)
    return render(request, 'jobs.html', {
        'jobs': all_jobs,
        'dept_choices': DEPT_CHOICES,
        'selected_dept': dept
    })


def job_detail(request, pk):
    return render(request, 'job_details.html', {'job': get_object_or_404(Job, pk=pk)})


def student_dashboard(request):
    return render(request, 'student/dashboard.html', {
        'title': 'Student Dashboard',
        'notices': Notice.objects.order_by('-created_at')[:10],
        'news': News.objects.order_by('-created_at')[:8],
    })


# ====================== CHATBOT ======================
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

        ChatMessage.objects.create(session_key=session_key, sender="user", message=user_message)

        context = ""
        try:
            from .rag import get_relevant_context
            context = get_relevant_context(user_message)
        except Exception:
            pass

        history = list(ChatMessage.objects.filter(session_key=session_key).order_by('-created_at')[:7])[::-1]
        history_text = "".join(f"{'User' if h.sender == 'user' else 'Assistant'}: {h.message}\n" for h in history[:-1])

        if context:
            prompt = f"You are the official AI Assistant for East West University (EWU).\nAnswer ONLY using the provided context.\n\nCONTEXT:\n{context}\n\nHISTORY:\n{history_text}User: {user_message}\nAssistant:"
        else:
            prompt = f"You are the official AI Assistant for East West University (EWU), Bangladesh.\nBe helpful and polite.\n\nHISTORY:\n{history_text}User: {user_message}\nAssistant:"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False, "options": {"temperature": 0.3, "num_predict": 500}},
            timeout=90,
        )
        reply = response.json().get("response", "").strip() if response.status_code == 200 else "Sorry, the AI is not responding."
        ChatMessage.objects.create(session_key=session_key, sender="bot", message=reply)
        return JsonResponse({"reply": reply})
    except Exception as e:
        print(f"[Chat Error] {e}")
        return JsonResponse({"reply": "Sorry, I'm having trouble right now. Please call 09666775577."})


# ====================== ADMIN AUTH ======================
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', '').strip(),
            password=request.POST.get('password', '')
        )
        if user and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('admin_dashboard')
        messages.error(request, "Invalid credentials or insufficient permissions.")

    return render(request, 'admin/admin_login.html')


@login_required(login_url='/admin/login/')
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('admin_login')


@_staff_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html', {
        'total_notices': Notice.objects.count(),
        'total_news': News.objects.count(),
        'total_sliders': Slider.objects.count(),
        'total_events': Event.objects.filter(is_active=True).count(),
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'total_achievements': Achievement.objects.filter(is_active=True).count(),
        'total_gallery': GalleryPhoto.objects.filter(is_active=True).count(),
        'recent_notices': Notice.objects.order_by('-created_at')[:5],
        'recent_news': News.objects.order_by('-created_at')[:5],
    })



# Notice CRUD
@_staff_required
def notice_list_admin(request):
    q = request.GET.get('q', '').strip()
    qs = Notice.objects.order_by('-created_at')
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'admin/notice_list.html', {'notices': qs, 'q': q})

@_staff_required
def notice_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('description', '').strip()
        if title and desc:
            Notice.objects.create(title=title, description=desc)
            messages.success(request, 'Notice published successfully.')
            return redirect('admin_notice_list')
        messages.error(request, 'Title and description required.')
    return render(request, 'admin/notice_form.html', {'edit': False})

@_staff_required
def notice_edit(request, pk):
    obj = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('description', '').strip()
        if title and desc:
            obj.title = title
            obj.description = desc
            obj.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('admin_notice_list')
        messages.error(request, 'Title and description required.')
    return render(request, 'admin/notice_form.html', {'obj': obj, 'edit': True})

@_staff_required
def notice_delete(request, pk):
    obj = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Notice deleted successfully.')
        return redirect('admin_notice_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Notice', 'cancel': 'admin_notice_list'})


# News CRUD
@_staff_required
def news_list_admin(request):
    q = request.GET.get('q', '').strip()
    qs = News.objects.order_by('-created_at')
    if q:
        qs = qs.filter(title__icontains=q)
    return render(request, 'admin/news_list.html', {'news_list': qs, 'q': q})

@_staff_required
def news_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        if title and desc and image:
            News.objects.create(title=title, description=desc, image=image)
            messages.success(request, 'News published successfully.')
            return redirect('admin_news_list')
        messages.error(request, 'Title, description and image required.')
    return render(request, 'admin/news_form.html', {'edit': False})

@_staff_required
def news_edit(request, pk):
    obj = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('description', '').strip()
        if title and desc:
            obj.title = title
            obj.description = desc
            if request.FILES.get('image'):
                obj.image = request.FILES['image']
            obj.save()
            messages.success(request, 'News updated successfully.')
            return redirect('admin_news_list')
        messages.error(request, 'Title and description required.')
    return render(request, 'admin/news_form.html', {'obj': obj, 'edit': True})

@_staff_required
def news_delete(request, pk):
    obj = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'News deleted successfully.')
        return redirect('admin_news_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'News', 'cancel': 'admin_news_list'})


# Slider CRUD
@_staff_required
def slider_list(request):
    sliders = Slider.objects.order_by('order', 'id')
    return render(request, 'admin/slider_list.html', {'sliders': sliders})

@_staff_required
def slider_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        badge = request.POST.get('badge', '').strip()
        order = int(request.POST.get('order', 0))
        image = request.FILES.get('image')
        if title and image:
            Slider.objects.create(title=title, subtitle=subtitle, badge=badge, order=order, image=image)
            messages.success(request, 'Slider created successfully.')
            return redirect('admin_slider_list')
        messages.error(request, 'Title and image required.')
    return render(request, 'admin/slider_form.html', {'edit': False})

@_staff_required
def slider_edit(request, pk):
    obj = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.subtitle = request.POST.get('subtitle', '').strip()
        obj.badge = request.POST.get('badge', '').strip()
        obj.order = int(request.POST.get('order', obj.order))
        if request.FILES.get('image'):
            obj.image = request.FILES['image']
        obj.save()
        messages.success(request, 'Slider updated successfully.')
        return redirect('admin_slider_list')
    return render(request, 'admin/slider_form.html', {'obj': obj, 'edit': True})

@_staff_required
def slider_delete(request, pk):
    obj = get_object_or_404(Slider, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Slider deleted successfully.')
        return redirect('admin_slider_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Slider', 'cancel': 'admin_slider_list'})


# Event CRUD
@_staff_required
def event_list(request):
    return render(request, 'admin/event_list.html', {'events': Event.objects.order_by('date')})

@_staff_required
def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date')
        location = request.POST.get('location', '').strip()
        desc = request.POST.get('description', '').strip()
        color = request.POST.get('badge_color', 'green')
        active = bool(request.POST.get('is_active'))
        if title and date:
            Event.objects.create(title=title, date=date, location=location,
                                 description=desc, badge_color=color, is_active=active)
            messages.success(request, 'Event created.')
            return redirect('admin_event_list')
        messages.error(request, 'Title and date required.')
    return render(request, 'admin/event_form.html', {'edit': False, 'color_choices': getattr(Event, 'BADGE_COLORS', [])})

@_staff_required
def event_edit(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.date = request.POST.get('date')
        obj.location = request.POST.get('location', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.badge_color = request.POST.get('badge_color', 'green')
        obj.is_active = bool(request.POST.get('is_active'))
        obj.save()
        messages.success(request, 'Event updated.')
        return redirect('admin_event_list')
    return render(request, 'admin/event_form.html', {'obj': obj, 'edit': True, 'color_choices': getattr(Event, 'BADGE_COLORS', [])})

@_staff_required
def event_delete(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Event deleted.')
        return redirect('admin_event_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Event', 'cancel': 'admin_event_list'})


# Important Date CRUD
@_staff_required
def date_list(request):
    return render(request, 'admin/date_list.html', {'dates': ImportantDate.objects.order_by('date')})

@_staff_required
def date_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date')
        category = request.POST.get('category', 'academic')
        note = request.POST.get('note', '').strip()
        active = bool(request.POST.get('is_active'))
        if title and date:
            ImportantDate.objects.create(title=title, date=date, category=category, note=note, is_active=active)
            messages.success(request, 'Important date added.')
            return redirect('admin_date_list')
        messages.error(request, 'Title and date required.')
    return render(request, 'admin/date_form.html', {'edit': False, 'cat_choices': getattr(ImportantDate, 'CATEGORY_CHOICES', [])})

@_staff_required
def date_edit(request, pk):
    obj = get_object_or_404(ImportantDate, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.date = request.POST.get('date')
        obj.category = request.POST.get('category', 'academic')
        obj.note = request.POST.get('note', '').strip()
        obj.is_active = bool(request.POST.get('is_active'))
        obj.save()
        messages.success(request, 'Date updated.')
        return redirect('admin_date_list')
    return render(request, 'admin/date_form.html', {'obj': obj, 'edit': True, 'cat_choices': getattr(ImportantDate, 'CATEGORY_CHOICES', [])})

@_staff_required
def date_delete(request, pk):
    obj = get_object_or_404(ImportantDate, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Date deleted.')
        return redirect('admin_date_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Important Date', 'cancel': 'admin_date_list'})


# Achievement CRUD
@_staff_required
def achievement_list(request):
    return render(request, 'admin/achievement_list.html', {'achievements': Achievement.objects.order_by('-achieved_on')})

@_staff_required
def achievement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        achieved_on = request.POST.get('achieved_on')
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        active = bool(request.POST.get('is_active'))
        if title and achieved_on:
            Achievement.objects.create(title=title, achieved_on=achieved_on,
                                       description=description, is_active=active,
                                       **({'image': image} if image else {}))
            messages.success(request, 'Achievement added.')
            return redirect('admin_achievement_list')
        messages.error(request, 'Title and date required.')
    return render(request, 'admin/achievement_form.html', {'edit': False})

@_staff_required
def achievement_edit(request, pk):
    obj = get_object_or_404(Achievement, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.achieved_on = request.POST.get('achieved_on')
        obj.description = request.POST.get('description', '').strip()
        obj.is_active = bool(request.POST.get('is_active'))
        if request.FILES.get('image'):
            obj.image = request.FILES['image']
        obj.save()
        messages.success(request, 'Achievement updated.')
        return redirect('admin_achievement_list')
    return render(request, 'admin/achievement_form.html', {'obj': obj, 'edit': True})

@_staff_required
def achievement_delete(request, pk):
    obj = get_object_or_404(Achievement, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Achievement deleted.')
        return redirect('admin_achievement_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Achievement', 'cancel': 'admin_achievement_list'})


# Job CRUD
@_staff_required
def job_list_admin(request):
    return render(request, 'admin/job_list.html', {'jobs': Job.objects.order_by('-id')})

@_staff_required
def job_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        department = request.POST.get('department', 'other')
        job_type = request.POST.get('job_type', 'full_time')
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        how_to_apply = request.POST.get('how_to_apply', '').strip()
        deadline = request.POST.get('deadline') or None
        active = bool(request.POST.get('is_active'))
        if title and description:
            Job.objects.create(title=title, department=department, job_type=job_type,
                               description=description, requirements=requirements,
                               how_to_apply=how_to_apply, deadline=deadline, is_active=active)
            messages.success(request, 'Job posting created.')
            return redirect('admin_job_list')
        messages.error(request, 'Title and description required.')
    return render(request, 'admin/job_form.html', {
        'edit': False,
        'dept_choices': getattr(Job, 'DEPT_CHOICES', DEPT_CHOICES),
        'type_choices': getattr(Job, 'TYPE_CHOICES', [])
    })

@_staff_required
def job_edit(request, pk):
    obj = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.department = request.POST.get('department', 'other')
        obj.job_type = request.POST.get('job_type', 'full_time')
        obj.description = request.POST.get('description', '').strip()
        obj.requirements = request.POST.get('requirements', '').strip()
        obj.how_to_apply = request.POST.get('how_to_apply', '').strip()
        obj.deadline = request.POST.get('deadline') or None
        obj.is_active = bool(request.POST.get('is_active'))
        obj.save()
        messages.success(request, 'Job updated.')
        return redirect('admin_job_list')
    return render(request, 'admin/job_form.html', {
        'obj': obj, 'edit': True,
        'dept_choices': getattr(Job, 'DEPT_CHOICES', DEPT_CHOICES),
        'type_choices': getattr(Job, 'TYPE_CHOICES', [])
    })

@_staff_required
def job_delete(request, pk):
    obj = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Job deleted.')
        return redirect('admin_job_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Job', 'cancel': 'admin_job_list'})


# Gallery CRUD
@_staff_required
def gallery_list_admin(request):
    return render(request, 'admin/gallery_list.html', {
        'photos': GalleryPhoto.objects.select_related('category').order_by('-uploaded_at'),
        'categories': GalleryCategory.objects.all(),
    })

@_staff_required
def gallery_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        caption = request.POST.get('caption', '').strip()
        cat_id = request.POST.get('category') or None
        active = bool(request.POST.get('is_active'))
        image = request.FILES.get('image')
        if title and image:
            cat = GalleryCategory.objects.filter(pk=cat_id).first() if cat_id else None
            GalleryPhoto.objects.create(title=title, caption=caption, category=cat, is_active=active, image=image)
            messages.success(request, 'Photo uploaded.')
            return redirect('admin_gallery_list')
        messages.error(request, 'Title and image required.')
    return render(request, 'admin/gallery_form.html', {
        'edit': False,
        'categories': GalleryCategory.objects.all()
    })

@_staff_required
def gallery_edit(request, pk):
    obj = get_object_or_404(GalleryPhoto, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.caption = request.POST.get('caption', '').strip()
        cat_id = request.POST.get('category') or None
        obj.category = GalleryCategory.objects.filter(pk=cat_id).first() if cat_id else None
        obj.is_active = bool(request.POST.get('is_active'))
        if request.FILES.get('image'):
            obj.image = request.FILES['image']
        obj.save()
        messages.success(request, 'Photo updated.')
        return redirect('admin_gallery_list')
    return render(request, 'admin/gallery_form.html', {
        'obj': obj, 'edit': True, 'categories': GalleryCategory.objects.all()
    })

@_staff_required
def gallery_delete(request, pk):
    obj = get_object_or_404(GalleryPhoto, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Photo deleted.')
        return redirect('admin_gallery_list')
    return render(request, 'admin/confirm_delete.html', {'obj': obj, 'type': 'Gallery Photo', 'cancel': 'admin_gallery_list'})