from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import StudentProfile

EWU_STUDENT_DOMAIN = 'gmail.com'


def student_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        email      = request.POST.get('email', '').strip().lower()
        #student_id = request.POST.get('student_id', '').strip()
        program    = request.POST.get('program', '')
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        ctx = {'programs': StudentProfile.PROGRAM_CHOICES}

        if not email.endswith(f'@{EWU_STUDENT_DOMAIN}'):
            messages.error(request, f'Only @{EWU_STUDENT_DOMAIN} emails are allowed.')
            return render(request, 'student/register.html', ctx)
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'student/register.html', ctx)
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'student/register.html', ctx)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'student/register.html', ctx)
        
        try:
            username = email.split('@')[0]
            base, counter = username, 1
            while User.objects.filter(username=username).exists():
                username = f'{base}{counter}'
                counter += 1

            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name,
            )
            StudentProfile.objects.create(user=user, program=program)
            messages.success(request, 'Account created! Please sign in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            print(e)

    return render(request, 'student/register.html', {'programs': StudentProfile.PROGRAM_CHOICES})


#now