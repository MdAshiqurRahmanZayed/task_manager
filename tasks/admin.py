from django.contrib import admin
from .models import *


# Include Admin in models
class TaskInline(admin.TabularInline):
     model = TaskPhoto
     extra = 1
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "priority", "is_complete", "created_at", "modified_at")
    readonly_fields = ('created_at', 'modified_at')  # Display these fields as read-only
 
    fieldsets = (
        ("Main", {'fields': ('user','description', 'title', 'due_date', 'priority', 'is_complete')}),
        ('Time Information', {'fields': ('created_at', 'modified_at')}),
    )
    inlines = [TaskInline]

admin.site.register(Task,TaskAdmin)
admin.site.register(TaskPhoto)
