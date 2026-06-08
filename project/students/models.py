from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    PROGRAM_CHOICES = [
        ('BSc_CSE',       'BSc in Computer Science & Engineering'),
        ('BSc_EEE',       'BSc in Electrical & Electronic Engineering'),
        ('BSc_CE',        'BSc in Civil Engineering'),
        ('BSc_GEB',       'BSc in Genetic Engineering & Biotechnology'),
        ('BSc_Pharmacy',  'BSc in Pharmacy'),
        ('BBA',           'Bachelor of Business Administration'),
        ('LLB',           'Bachelor of Laws (LLB)'),
        ('BA_English',    'BA in English'),
        ('BA_SocialRel',  'BA in Social Relations'),
        ('BSc_InfoStudy', 'BSc in Information Studies'),
        ('BSc_Sociology', 'BSc in Sociology'),
        ('BSc_Economics', 'BSc in Economics'),
        ('MBA',           'Master of Business Administration'),
        ('EMBA',          'Executive MBA'),
        ('MSc_CSE',       'MSc in Computer Science & Engineering'),
        ('LLM',           'Master of Laws (LLM)'),
        ('MA_English',    'MA in English'),
    ]

    SEMESTER_CHOICES = [
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall',   'Fall'),
    ]

    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id   = models.CharField(max_length=20, unique=True, help_text='e.g. 2021-1-60-001')
    program      = models.CharField(max_length=30, choices=PROGRAM_CHOICES, default='BSc_CSE')
    semester     = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='Spring')
    year         = models.IntegerField(default=2024)
    phone        = models.CharField(max_length=20, blank=True)
    profile_pic  = models.ImageField(upload_to='students/pics/', blank=True, null=True)
    date_of_birth= models.DateField(null=True, blank=True)
    address      = models.TextField(blank=True)
    is_verified  = models.BooleanField(default=False, help_text='Email verified')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.student_id} — {self.user.get_full_name() or self.user.username}"

    @property
    def email(self):
        return self.user.email

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username