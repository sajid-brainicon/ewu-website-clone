from django.db import models


class Slider(models.Model):
    title    = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image    = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.title


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