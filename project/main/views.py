import datetime
import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Slider, Notice, News, Event, ImportantDate, ChatMessage

# ── Gemini system prompt ──────────────────────────────────────
EWU_SYSTEM_PROMPT = """
You are the official AI Assistant for East West University (EWU), Dhaka, Bangladesh.
Answer students' questions accurately and helpfully.

Key facts:
- Location: A/2 Jahurul Islam Avenue, Aftabnagar, Dhaka-1212, Bangladesh
- Phone: 09666775577 | Email: admissions@ewubd.edu | Website: www.ewubd.edu
- Vice Chancellor: Professor Shams Rahman
- Chairperson, Board of Trustees: Professor Dr. Mohammed Farashuddin
- Departments: CSE, EEE, BBA, Pharmacy, Economics, English, Law, Architecture
- 29 programs: BSc CSE, BSc EEE, BBA, MBA, EMBA, BSc Pharmacy, LLB, etc.
- Scholarships: 50% to 100% merit-based during admission
- MBA deadline (Summer 2026): April 17 | EMBA deadline: April 18
- For unknown fees/schedules, direct users to admissions@ewubd.edu
Keep answers concise, friendly, professional.
Reply in the same language the user writes in.
""".strip()


# ══════════════════════════════════════════
#  PAGE VIEWS
# ══════════════════════════════════════════

def home(request):
    sliders = Slider.objects.all()
    notices = Notice.objects.all()[:5]
    news_list = News.objects.all()[:4]
    events = Event.objects.filter(is_active=True).order_by('date')[:5]
    important_dates = ImportantDate.objects.filter(
        date__gte=datetime.date.today(),
        is_active=True,
    ).order_by('date')[:5]

    return render(request, 'home.html', {
        'sliders':         sliders,
        'notices':         notices,
        'news_list':       news_list,
        'events':          events,
        'important_dates': important_dates,
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
        {'name': 'Computer Science & Engineering',      'icon': 'fa-laptop-code',     'desc': 'AI, ML, software engineering and more.'},
        {'name': 'Electrical & Electronic Engineering', 'icon': 'fa-bolt',            'desc': 'Power systems, electronics, and telecom.'},
        {'name': 'Business Administration',             'icon': 'fa-chart-line',      'desc': 'Management, finance, marketing.'},
        {'name': 'Pharmacy',                            'icon': 'fa-capsules',        'desc': 'Pharmaceutical sciences and clinical research.'},
        {'name': 'Economics',                           'icon': 'fa-coins',           'desc': 'Micro/macro economics and econometrics.'},
        {'name': 'English',                             'icon': 'fa-book-open',       'desc': 'Language, literature, and linguistics.'},
        {'name': 'Law',                                 'icon': 'fa-gavel',           'desc': 'Legal studies and justice administration.'},
        {'name': 'Architecture',                        'icon': 'fa-drafting-compass','desc': 'Design, planning, and sustainable architecture.'},
    ]
    return render(request, 'departments.html', {'departments': departments_list})


def faculty(request):
    faculty_members = [
        {'name': 'Dr. Ahmed Hossain',    'designation': 'Professor, CSE',           'image': 'images/placeholder.jpg'},
        {'name': 'Prof. Nusrat Jahan',   'designation': 'Chairperson, EEE',         'image': 'images/placeholder.jpg'},
        {'name': 'Dr. Kamal Uddin',      'designation': 'Associate Professor, BBA', 'image': 'images/placeholder.jpg'},
        {'name': 'Dr. Farhana Rahman',   'designation': 'Professor, Pharmacy',      'image': 'images/placeholder.jpg'},
        {'name': 'Md. Rafiqul Islam',    'designation': 'Lecturer, Economics',      'image': 'images/placeholder.jpg'},
        {'name': 'Prof. Sharmin Akhter', 'designation': 'Dean, Arts & Humanities',  'image': 'images/placeholder.jpg'},
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


# ══════════════════════════════════════════
#  CHAT VIEW
# ══════════════════════════════════════════

def _smart_fallback(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in ['admission', 'apply', 'enroll']):
        return "To apply, visit our Admissions page or email admissions@ewubd.edu. Call 09666775577 for help."
    if any(w in msg for w in ['scholarship', 'waiver', 'financial']):
        return "EWU offers merit scholarships from 50% to 100% of tuition during admission."
    if any(w in msg for w in ['fee', 'tuition', 'cost']):
        return "Fees vary by department. Please email admissions@ewubd.edu for exact figures."
    if any(w in msg for w in ['hello', 'hi', 'hey', 'salam']):
        return "Hello! I'm the EWU AI Assistant. How can I help you today?"
    return "For detailed information please contact admissions@ewubd.edu or call 09666775577 (Sun–Thu, 9 AM–5 PM)."


@csrf_exempt
def chat_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required.'}, status=405)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'reply': 'Invalid request format.'}, status=400)

    user_message = (data.get('message') or '').strip()
    if not user_message:
        return JsonResponse({'reply': 'Please type a message.'})

    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    ChatMessage.objects.create(session_key=session_key, sender='user', message=user_message)

    history = list(
        ChatMessage.objects
        .filter(session_key=session_key)
        .order_by('-created_at')[:11]
    )
    history.reverse()
    history = history[:-1]

    reply = None
    api_key = getattr(settings, 'GEMINI_API_KEY', None)

    if api_key and api_key != 'GEMINI_API_KEY':
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            contents = []
            for h in history:
                role = 'user' if h.sender == 'user' else 'model'
                contents.append(types.Content(role=role, parts=[types.Part(text=h.message)]))
            contents.append(types.Content(role='user', parts=[types.Part(text=user_message)]))

            response = client.models.generate_content(
                model = genai.GenerativeModel("gemini-2.5-flash"),
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=EWU_SYSTEM_PROMPT,
                    max_output_tokens=500,
                    temperature=0.7,
                ),
            )
            reply = response.text.strip() if response.text else None

        except ImportError:
            print('[EWU Chat] Run: pip install google-genai')
        except Exception as e:
            print(f'[EWU Chat] Gemini error: {type(e).__name__}: {e}')
    else:
        print('[EWU Chat] GEMINI_API_KEY not set in settings.py')

    if not reply:
        reply = _smart_fallback(user_message)

    ChatMessage.objects.create(session_key=session_key, sender='bot', message=reply)
    return JsonResponse({'reply': reply})