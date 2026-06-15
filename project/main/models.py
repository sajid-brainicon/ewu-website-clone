from django.db import models
from django.contrib.contenttypes.models import ContentType


class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    badge = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='sliders/')
    order = models.PositiveIntegerField(default=0)  
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Notice(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class News(models.Model):
    title       = models.CharField(max_length=200)
    image       = models.ImageField(upload_to='news/', blank=True, null=True)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class Event(models.Model):
    BADGE_COLORS = [
        ('green',  'Green'),
        ('red',    'Red'),
        ('blue',   'Blue'),
        ('orange', 'Orange'),
    ]
    title       = models.CharField(max_length=300)
    date        = models.DateField()
    location    = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    badge_color = models.CharField(max_length=10, choices=BADGE_COLORS, default='green')
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} — {self.date}"


class ImportantDate(models.Model):
    CATEGORY_CHOICES = [
        ('academic',  'Academic Calendar'),
        ('exam',      'Examination'),
        ('holiday',   'Holiday'),
        ('admission', 'Admission'),
        ('result',    'Result'),
        ('other',     'Other'),
    ]
    title     = models.CharField(max_length=300)
    date      = models.DateField()
    category  = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    note      = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Important Date'

    def __str__(self):
        return f"{self.title} — {self.date}"


# ── FIXED: single ChatMessage class (you had it defined twice) ──
class ChatMessage(models.Model):
    SENDER_CHOICES = [('user', 'User'), ('bot', 'Bot')]

    session_key = models.CharField(max_length=40, db_index=True)
    sender      = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender}] {self.message[:60]}"
    
class Achievement(models.Model):
    title       = models.CharField(max_length=400)
    achieved_on = models.DateField()
    image       = models.ImageField(upload_to='achievements/')   
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
 
    class Meta:
        ordering = ['-achieved_on']
 
    def __str__(self):
        return f"{self.title} — {self.achieved_on}"
    


class GalleryCategory(models.Model):
    name  = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
 
    class Meta:
        ordering     = ['order']
        verbose_name = 'Gallery Category'
        verbose_name_plural = 'Gallery Categories'
 
    def __str__(self):
        return self.name
 
 
class GalleryPhoto(models.Model):
    title    = models.CharField(max_length=200)
    image    = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='photos'
    )
    caption    = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)
 
    class Meta:
        ordering     = ['-uploaded_at']
        verbose_name = 'Gallery Photo'
 
    def __str__(self):
        return self.title
 
 
class Job(models.Model):
    TYPE_CHOICES = [
        ('full_time',  'Full Time'),
        ('part_time',  'Part Time'),
        ('contractual','Contractual'),
        ('adjunct',    'Adjunct'),
    ]
    DEPT_CHOICES = [
        ('cse',       'CSE'),
        ('eee',       'EEE'),
        ('bba',       'BBA'),
        ('pharmacy',  'Pharmacy'),
        ('economics', 'Economics'),
        ('english',   'English'),
        ('law',       'Law'),
        ('admin',     'Administration'),
        ('other',     'Other'),
    ]
 
    title           = models.CharField(max_length=200)
    department      = models.CharField(max_length=20, choices=DEPT_CHOICES, default='other')
    job_type        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full_time')
    description     = models.TextField(help_text='Full job description. Supports plain text.')
    requirements    = models.TextField(blank=True, help_text='One requirement per line.')
    how_to_apply    = models.TextField(blank=True, help_text='Application instructions.')
    deadline        = models.DateField(null=True, blank=True)
    posted_at       = models.DateTimeField(auto_now_add=True)
    is_active       = models.BooleanField(default=True)
 
    class Meta:
        ordering     = ['-posted_at']
        verbose_name = 'Job Opening'
 
    def __str__(self):
        return f"{self.title} — {self.get_department_display()}"
 
    def is_expired(self):
        import datetime
        if self.deadline:
            return self.deadline < datetime.date.today()
        return False
 
    def requirements_list(self):
        if self.requirements:
            return [r.strip() for r in self.requirements.splitlines() if r.strip()]
        return []



class ManagedModule(models.Model):
    content_type = models.OneToOneField(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'app_label': 'main'},
    )
    display_name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'display_name']

    def __str__(self):
        return self.display_name