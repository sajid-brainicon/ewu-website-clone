from django.contrib import admin
from .models import Slider, Notice, News, Event, ImportantDate, ChatMessage


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