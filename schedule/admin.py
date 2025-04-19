from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day', 'start_time', 'end_time', 'room', 'user')
    list_filter = ('day', 'user')
    search_fields = ('subject', 'room', 'professor')