from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('resend-code/', views.resend_verification_code, name='resend_verification_code'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('', views.notes_list, name='notes_list'),
    path('detail/<slug:slug>/', views.detail, name='detail'),
    path('add/', views.add_note, name='add_note'),
    path('note/<int:note_id>/', views.detail_by_id, name='detail_by_id'),  # Add this
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),  # Add this
    path('api/notes/', views.NoteListCreateView.as_view(), name='note-list'),
    path('api/notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
]