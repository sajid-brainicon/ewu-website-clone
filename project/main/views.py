import datetime
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Slider, Notice, News, Event, ImportantDate, ChatMessage


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
        {'name': 'Computer Science & Engineering',      'icon': 'fa-laptop-code',      'desc': 'AI, ML, software engineering and more.'},
        {'name': 'Electrical & Electronic Engineering', 'icon': 'fa-bolt',             'desc': 'Power systems, electronics, and telecom.'},
        {'name': 'Business Administration',             'icon': 'fa-chart-line',       'desc': 'Management, finance, marketing.'},
        {'name': 'Pharmacy',                            'icon': 'fa-capsules',         'desc': 'Pharmaceutical sciences and clinical research.'},
        {'name': 'Economics',                           'icon': 'fa-coins',            'desc': 'Micro/macro economics and econometrics.'},
        {'name': 'English',                             'icon': 'fa-book-open',        'desc': 'Language, literature, and linguistics.'},
        {'name': 'Law',                                 'icon': 'fa-gavel',            'desc': 'Legal studies and justice administration.'},
        {'name': 'Architecture',                        'icon': 'fa-drafting-compass', 'desc': 'Design, planning, and sustainable architecture.'},
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

@csrf_exempt
def chat_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"reply": "Please type a message."})

        # Session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # Save user message
        ChatMessage.objects.create(
            session_key=session_key,
            sender="user",
            message=user_message
        )

        # Get RAG context from PDF
        context = ""
        try:
            from .rag import get_relevant_context
            context = get_relevant_context(user_message)
            print(f"=== CONTEXT LENGTH: {len(context)} ===")
            print(f"=== CONTEXT PREVIEW: {context[:500]} ===")  # show what was found
            print(f"RAG context length: {len(context)}")
        except Exception as rag_err:
            print(f"RAG error (continuing without context): {rag_err}")

        # Get conversation history
        history = list(ChatMessage.objects.filter(
            session_key=session_key
        ).order_by('-created_at')[:6])[::-1]

        history_text = ""
        for h in history[:-1]:
            role = "User" if h.sender == "user" else "Assistant"
            history_text += f"{role}: {h.message}\n"

        # Build strict RAG prompt
        if context:
            prompt = f"""You are the official AI Assistant for East West University (EWU), Dhaka, Bangladesh.

STRICT RULES:
1. Answer ONLY using the CONTEXT provided below.
2. Do NOT use your training data or outside knowledge.
3. If the answer is NOT in the context, say exactly:
   "I don't have that information in my documents. Please contact EWU at 09666775577 or email info@ewubd.edu"
4. Keep answers concise and friendly.
5. Reply in the same language the user writes in (English or Bengali).

CONTEXT FROM EWU OFFICIAL DOCUMENTS:
{context}

CONVERSATION HISTORY:
{history_text}
User: {user_message}
Assistant:"""
        else:
            # No PDF context — use basic facts only
            prompt = f"""You are the official AI Assistant for East West University (EWU), Dhaka, Bangladesh.

STRICT RULES:
1. Only answer using the facts listed below. Do NOT make up information.
2. If you don't know the answer from these facts, say:
   "I don't have that information. Please contact EWU at 09666775577 or email info@ewubd.edu"
3. Keep answers concise and friendly.
4. Reply in the same language the user writes in (English or Bengali).

KNOWN EWU FACTS:
- Location: A/2 Jahurul Islam Avenue, Aftabnagar, Dhaka-1212, Bangladesh
- Phone: 09666775577 | Hotline: +8801755587224
- Email: info@ewubd.edu | Admissions: admissions@ewubd.edu
- Website: www.ewubd.edu
- Vice Chancellor: Professor Shams Rahman
- Chairperson, Board of Trustees: Professor Dr. Mohammed Farashuddin
- Departments: CSE, EEE, BBA, Pharmacy, Economics, English, Law, Civil Engineering, GEB
- Programs: BSc CSE, BSc EEE, BBA, MBA, EMBA, BSc Pharmacy, LLB and more (29 total)
- Scholarships: 50% to 100% merit-based during admission
- Office hours: Sunday to Thursday, 9 AM to 5 PM

CONVERSATION HISTORY:
{history_text}
User: {user_message}
Assistant:"""

        # Call Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,   # lower = more focused on context
                    "num_predict": 500,
                    "top_p": 0.9,
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            reply = response.json().get("response", "").strip()
            if not reply:
                reply = "I couldn't generate a response. Please try again."
        else:
            print(f"Ollama error: {response.status_code} {response.text}")
            reply = "Sorry, the AI model is not responding. Please try again."

        # Save bot reply
        ChatMessage.objects.create(
            session_key=session_key,
            sender="bot",
            message=reply
        )

        return JsonResponse({"reply": reply})

    except requests.exceptions.ConnectionError:
        return JsonResponse({
            "reply": "Cannot connect to Ollama. Make sure Ollama is running on your PC."
        })
    except requests.exceptions.Timeout:
        return JsonResponse({
            "reply": "The AI is taking too long to respond. Please try again."
        })
    except Exception as e:
        import traceback
        print(f"CHAT ERROR: {e}")
        print(traceback.format_exc())
        return JsonResponse({
            "reply": "Something went wrong. Please try again."
        })