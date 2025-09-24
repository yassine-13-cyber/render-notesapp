from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm,SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from .serializers import NoteSerializer



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
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    
    context = {'form': form}
    return render(request, 'registration/signup.html', context)




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
            messages.info(request, 'Invalid username or password.')
            
    context = {}
    return render(request, 'registration/login.html', context)


def logoutpage(request):
    logout(request)
    return redirect('login')