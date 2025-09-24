from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import User
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:  # If title has no valid characters for slug
                base_slug = f"note-{uuid.uuid4().hex[:8]}"
            
            # Ensure uniqueness
            slug = base_slug
            counter = 1
            while Note.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']