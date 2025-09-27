from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone   # ✅ fixed
import uuid
import random
import string
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(null=True, blank=True)

    def generate_verification_code(self):
        code = ''.join(random.choices(string.digits, k=6))
        self.email_verification_code = code
        self.code_created_at = timezone.now()
        self.save()
        return code

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
            base_slug = slugify(self.title) or f"note-{uuid.uuid4().hex[:8]}"
            slug = base_slug
            counter = 1
            while Note.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
