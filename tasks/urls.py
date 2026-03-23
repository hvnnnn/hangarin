from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),  # This name must match your template!
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('reminders/', views.reminders_view, name='reminders'),
    path('toggle/<int:task_id>/', views.toggle_task_status, name='toggle_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'), # Added for CRUD
    path('signup/', views.signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('notes/', views.note_list, name='note_list'),
    path('notes/add/', views.note_add, name='note_add'),
    path('notes/delete/<int:pk>/', views.note_delete, name='note_delete'),
]