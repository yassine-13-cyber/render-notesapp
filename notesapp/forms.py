# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, CustomUser

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'active', 'tags']

class SignUpForm(UserCreationForm):
    # This field is required, so we define it explicitly
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # UserCreationForm already handles username. Just add the email field.
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class EmailVerificationForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code'})
    )