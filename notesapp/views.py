from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Note
from .forms import NoteForm,SignUpForm,EmailVerificationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from .serializers import NoteSerializer
from django.utils import timezone   # Django’s timezone with .now()
from datetime import timedelta      # only timedelta comes from datetime
# notesapp/views.py
from .utils import send_verification_email # Add this import at the top
#@login_required(login_url='login')
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
    
    
#@login_required(login_url='login')
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


@login_required(login_url='login')
def notes_list(request):
    notes = Note.objects.filter(user=request.user,active=True)
    return render(request, 'notes_list.html', {'notes': notes})



@login_required(login_url='login')
def detail(request, slug):
    note = get_object_or_404(Note, slug=slug)
    return render(request, 'detail.html', {'note': note})


@login_required(login_url='login')
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            form.save()
            form.save_m2m()
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})


@login_required(login_url='login')
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id,user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            updated_note = form.save()
            return redirect('detail', slug=updated_note.slug)
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form, 'note': note})



@login_required(login_url='login')
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('notes_list')



@login_required(login_url='login')
def detail_by_id(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'detail.html', {'note': note})



def signup(request):
    if request.user.is_authenticated:
        return redirect('notes_list')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User can't login until email is verified
            user.save()
            
            # Generate and send verification code
            verification_code = user.generate_verification_code()
            send_verification_email(user.email, verification_code)
            
            # Store user ID in session for verification step
            request.session['pending_user_id'] = user.id
            return redirect('verify_email')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

def verify_email(request):
    # Check if there's a pending user in session
    pending_user_id = request.session.get('pending_user_id')
    if not pending_user_id:
        return redirect('register')
    
    try:
        pending_user = CustomUser.objects.get(id=pending_user_id)
    except CustomUser.DoesNotExist:
        return redirect('register')
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            
            # Check if code matches and is not expired (15 minutes)
            if (pending_user.email_verification_code == entered_code and
                pending_user.code_created_at and
                timezone.now() - pending_user.code_created_at < timedelta(minutes=15)):
                
                # Mark email as verified and activate user
                pending_user.is_email_verified = True
                pending_user.is_active = True
                pending_user.email_verification_code = None
                pending_user.code_created_at = None
                pending_user.save()
                
                # Log the user in
                login(request, pending_user)
                
                # Clean up session
                if 'pending_user_id' in request.session:
                    del request.session['pending_user_id']
                
                messages.success(request, 'Email verified successfully!')
                return redirect('notes_list')
            else:
                messages.error(request, 'Invalid or expired verification code.')
    else:
        form = EmailVerificationForm()
    
    return render(request, 'registration/verify_email.html', {
        'form': form,   # ❌ fixed (was `'form': form'`)
        'email': pending_user.email
    })

def resend_verification_code(request):
    pending_user_id = request.session.get('pending_user_id')
    if pending_user_id:
        try:
            user = CustomUser.objects.get(id=pending_user_id)
            new_code = user.generate_verification_code()
            send_verification_email(user.email, new_code)
            messages.info(request, 'New verification code sent!')
        except CustomUser.DoesNotExist:
            pass
    
    return redirect('verify_email')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('notes_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('notes_list')
        else:
            # Redirect directly to your custom error page
            return render(request, 'registration/you.html')

    return render(request, 'registration/login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')