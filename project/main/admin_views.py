"""
main/admin_views.py
Custom admin dashboard views for EWU website.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Notice, News, Event, ImportantDate, Slider


# ── Helper: only staff/superuser can access ──────────────────────
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def admin_required(view_func):
    return login_required(
        user_passes_test(is_admin, login_url='/dashboard/login/')(view_func),
        login_url='/dashboard/login/'
    )


# ══════════════════════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════════════════════

def admin_login_view(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin_dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid credentials or insufficient permissions.'

    return render(request, 'dashboard/admin_login.html', {'error': error})


def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


# ══════════════════════════════════════════════════════════════════
#  DASHBOARD HOME
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_dashboard_view(request):
    context = {
        'active': 'dashboard',
        'notice_count':  Notice.objects.count(),
        'news_count':    News.objects.count(),
        'event_count':   Event.objects.count(),
        'slider_count':  Slider.objects.count(),
        'recent_notices': Notice.objects.order_by('-created_at')[:5],
        'recent_news':    News.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ══════════════════════════════════════════════════════════════════
#  NOTICE CRUD
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'dashboard/admin_notice_list.html', {
        'notices': notices,
        'active': 'notices',
    })


@admin_required
def admin_notice_create(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title and description:
            Notice.objects.create(title=title, description=description)
            messages.success(request, 'Notice created successfully.')
            return redirect('admin_notice_list')
        else:
            messages.error(request, 'Title and description are required.')

    return render(request, 'dashboard/admin_notice_form.html', {'active': 'notices'})


@admin_required
def admin_notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title and description:
            notice.title       = title
            notice.description = description
            notice.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('admin_notice_list')
        else:
            messages.error(request, 'Title and description are required.')

    return render(request, 'dashboard/admin_notice_form.html', {
        'notice': notice,
        'active': 'notices',
    })


@admin_required
def admin_notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.success(request, f'Notice "{notice.title}" deleted.')
    return redirect('admin_notice_list')


# ══════════════════════════════════════════════════════════════════
#  NEWS CRUD
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_news_list(request):
    news_list = News.objects.order_by('-created_at')
    return render(request, 'dashboard/admin_news_list.html', {
        'news_list': news_list,
        'active': 'news',
    })


@admin_required
def admin_news_create(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image       = request.FILES.get('image')

        if title and description:
            news = News(title=title, description=description)
            if image:
                news.image = image
            news.save()
            messages.success(request, 'News article created successfully.')
            return redirect('admin_news_list')
        else:
            messages.error(request, 'Title and description are required.')

    return render(request, 'dashboard/admin_news_form.html', {'active': 'news'})


@admin_required
def admin_news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image       = request.FILES.get('image')

        if title and description:
            news.title       = title
            news.description = description
            if image:
                news.image = image
            news.save()
            messages.success(request, 'News article updated successfully.')
            return redirect('admin_news_list')
        else:
            messages.error(request, 'Title and description are required.')

    return render(request, 'dashboard/admin_news_form.html', {
        'news': news,
        'active': 'news',
    })


@admin_required
def admin_news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    messages.success(request, f'News article "{news.title}" deleted.')
    return redirect('admin_news_list')


# ══════════════════════════════════════════════════════════════════
#  EVENT CRUD (basic — expand as needed)
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_event_list(request):
    events = Event.objects.order_by('date')
    return render(request, 'dashboard/admin_event_list.html', {
        'events': events,
        'active': 'events',
    })


@admin_required
def admin_event_create(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        date        = request.POST.get('date', '').strip()
        location    = request.POST.get('location', '').strip()
        description = request.POST.get('description', '').strip()
        badge_color = request.POST.get('badge_color', 'green')
        is_active   = request.POST.get('is_active') == 'on'

        if title and date:
            Event.objects.create(
                title=title, date=date, location=location,
                description=description, badge_color=badge_color, is_active=is_active
            )
            messages.success(request, 'Event created successfully.')
            return redirect('admin_event_list')
        else:
            messages.error(request, 'Title and date are required.')

    return render(request, 'dashboard/admin_event_form.html', {'active': 'events'})


@admin_required
def admin_event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event.title       = request.POST.get('title', '').strip()
        event.date        = request.POST.get('date', '').strip()
        event.location    = request.POST.get('location', '').strip()
        event.description = request.POST.get('description', '').strip()
        event.badge_color = request.POST.get('badge_color', 'green')
        event.is_active   = request.POST.get('is_active') == 'on'

        if event.title and event.date:
            event.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('admin_event_list')
        else:
            messages.error(request, 'Title and date are required.')

    return render(request, 'dashboard/admin_event_form.html', {
        'event': event,
        'active': 'events',
    })


@admin_required
def admin_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, f'Event "{event.title}" deleted.')
    return redirect('admin_event_list')


# ══════════════════════════════════════════════════════════════════
#  SLIDER CRUD
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_slider_list(request):
    sliders = Slider.objects.all()
    return render(request, 'dashboard/admin_slider_list.html', {
        'sliders': sliders,
        'active': 'sliders',
    })


@admin_required
def admin_slider_create(request):
    if request.method == 'POST':
        title    = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        image    = request.FILES.get('image')

        if title and image:
            Slider.objects.create(title=title, subtitle=subtitle, image=image)
            messages.success(request, 'Slider created successfully.')
            return redirect('admin_slider_list')
        else:
            messages.error(request, 'Title and image are required.')

    return render(request, 'dashboard/admin_slider_form.html', {'active': 'sliders'})


@admin_required
def admin_slider_edit(request, pk):
    slider = get_object_or_404(Slider, pk=pk)

    if request.method == 'POST':
        slider.title    = request.POST.get('title', '').strip()
        slider.subtitle = request.POST.get('subtitle', '').strip()
        image = request.FILES.get('image')
        if image:
            slider.image = image
        if slider.title:
            slider.save()
            messages.success(request, 'Slider updated successfully.')
            return redirect('admin_slider_list')
        else:
            messages.error(request, 'Title is required.')

    return render(request, 'dashboard/admin_slider_form.html', {
        'slider': slider,
        'active': 'sliders',
    })


@admin_required
def admin_slider_delete(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    slider.delete()
    messages.success(request, 'Slider deleted.')
    return redirect('admin_slider_list')


# ══════════════════════════════════════════════════════════════════
#  IMPORTANT DATE CRUD
# ══════════════════════════════════════════════════════════════════

@admin_required
def admin_date_list(request):
    dates = ImportantDate.objects.order_by('date')
    return render(request, 'dashboard/admin_date_list.html', {
        'dates': dates,
        'active': 'dates',
    })


@admin_required
def admin_date_create(request):
    if request.method == 'POST':
        title    = request.POST.get('title', '').strip()
        date     = request.POST.get('date', '').strip()
        category = request.POST.get('category', 'academic')
        note     = request.POST.get('note', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        if title and date:
            ImportantDate.objects.create(
                title=title, date=date,
                category=category, note=note, is_active=is_active
            )
            messages.success(request, 'Important date created successfully.')
            return redirect('admin_date_list')
        else:
            messages.error(request, 'Title and date are required.')

    return render(request, 'dashboard/admin_date_form.html', {'active': 'dates'})


@admin_required
def admin_date_edit(request, pk):
    date_obj = get_object_or_404(ImportantDate, pk=pk)

    if request.method == 'POST':
        date_obj.title    = request.POST.get('title', '').strip()
        date_obj.date     = request.POST.get('date', '').strip()
        date_obj.category = request.POST.get('category', 'academic')
        date_obj.note     = request.POST.get('note', '').strip()
        date_obj.is_active = request.POST.get('is_active') == 'on'

        if date_obj.title and date_obj.date:
            date_obj.save()
            messages.success(request, 'Important date updated successfully.')
            return redirect('admin_date_list')
        else:
            messages.error(request, 'Title and date are required.')

    return render(request, 'dashboard/admin_date_form.html', {
        'date_obj': date_obj,
        'active': 'dates',
    })


@admin_required
def admin_date_delete(request, pk):
    date_obj = get_object_or_404(ImportantDate, pk=pk)
    date_obj.delete()
    messages.success(request, 'Important date deleted.')
    return redirect('admin_date_list')


# ══════════════════════════════════════════════════════════════════
#  STUDENT DASHBOARD (placeholder)
# ══════════════════════════════════════════════════════════════════

def student_dashboard_view(request):
    import datetime
    context = {
        'notice_count': Notice.objects.count(),
        'news_count':   News.objects.count(),
        'event_count':  Event.objects.filter(is_active=True).count(),
        'date_count':   ImportantDate.objects.filter(
            is_active=True, date__gte=datetime.date.today()
        ).count(),
    }
    return render(request, 'dashboard/student_dashboard.html', context)