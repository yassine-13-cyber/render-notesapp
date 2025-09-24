from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'slug', 'active', 'created_at', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['active']
    ordering = ['-updated_at']
    readonly_fields = ['slug']  # Make slug read-only since it's auto-generated
    
    # Make sure all fields are editable
    fields = ['user','title', 'slug', 'content', 'tags', 'active']