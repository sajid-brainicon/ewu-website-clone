from django.contrib import admin
from django.utils.html import format_html
from .models import Slider, Notice, News, Event, ImportantDate, ChatMessage, Achievement, GalleryCategory, GalleryPhoto, Job


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle']


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'badge_color', 'is_active']
    list_filter  = ['badge_color', 'is_active']


@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'category']
    list_filter  = ['category']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display    = ['session_key', 'sender', 'short_message', 'created_at']
    list_filter     = ['sender']
    search_fields   = ['session_key', 'message']
    ordering        = ['-created_at']
    readonly_fields = ['session_key', 'sender', 'message', 'created_at']

    def short_message(self, obj):
        return obj.message[:80] + ('…' if len(obj.message) > 80 else '')
    short_message.short_description = 'Message'

    def has_add_permission(self, request):
        return False
    
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display   = ['title', 'achieved_on', 'is_active']
    list_editable  = ['is_active']
    list_filter    = ['is_active']
    search_fields  = ['title']
    ordering       = ['-achieved_on']
    date_hierarchy = 'achieved_on'

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'order', 'photo_count']
    list_editable = ['order']
    ordering      = ['order']
 
    def photo_count(self, obj):
        return obj.photos.filter(is_active=True).count()
    photo_count.short_description = 'Photos'
 
 
class GalleryPhotoInline(admin.TabularInline):
    model  = GalleryPhoto
    extra  = 3
    fields = ['image', 'title', 'caption', 'is_active', 'thumb']
    readonly_fields = ['thumb']
 
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;border-radius:3px">', obj.image.url)
        return '—'
    thumb.short_description = 'Preview'
 
 
@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display   = ['thumb', 'title', 'category', 'is_active', 'uploaded_at']
    list_filter    = ['category', 'is_active']
    list_editable  = ['is_active']
    search_fields  = ['title', 'caption']
    ordering       = ['-uploaded_at']
    readonly_fields = ['thumb_large', 'uploaded_at']
 
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'thumb_large', 'category', 'caption', 'is_active')
        }),
        ('Info', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',),
        }),
    )
 
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;width:70px;object-fit:cover;border-radius:3px">', obj.image.url)
        return '—'
    thumb.short_description = 'Preview'
 
    def thumb_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:4px;margin-top:6px">', obj.image.url)
        return '—'
    thumb_large.short_description = 'Current Image'
 
 
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ['title', 'department', 'job_type', 'deadline', 'is_active', 'posted_at']
    list_filter   = ['department', 'job_type', 'is_active']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    ordering      = ['-posted_at']
 
    fieldsets = (
        ('Job Info', {
            'fields': ('title', 'department', 'job_type', 'is_active', 'deadline')
        }),
        ('Content', {
            'fields': ('description', 'requirements', 'how_to_apply')
        }),
    )