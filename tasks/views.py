from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone 
from datetime import timedelta
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Note


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) 
            task.user = request.user     
            task.save()                    
            return redirect('task_list')  
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


def delete_task(request, task_id):  # <--- Make sure 'task_id' is here!
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
    
@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('deadline') # Due soonest first

    # Search Logic
    search_query = request.GET.get('search')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Status Filter Logic (Updated from Priority to Status)
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task) # 'instance' is the key here!
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/add_task.html', {'form': form, 'edit_mode': True})

def reminders_view(request):
    now = timezone.now()
    
    # Clean version (removed the [cite] text)
    overdue = Task.objects.filter(deadline__lt=now).exclude(status="Completed")
    
    tomorrow = now + timedelta(days=1)
    upcoming = Task.objects.filter(deadline__range=(now, tomorrow)).exclude(status="Completed")

    return render(request, 'tasks/reminders.html', {
        'overdue': overdue,
        'upcoming': upcoming,
        'urgent_count': overdue.count() + upcoming.count()
    })

def toggle_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == 'Completed':
        task.status = 'Pending'
    else:
        task.status = 'Completed'
    task.save()
    return redirect('task_list')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Make sure the line below starts exactly under 'login'
            messages.success(request, "🎉 Welcome to Hangarin! Your account was created successfully.") 
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# 1. List all notes
@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/note_list.html', {'notes': notes})

# 2. Add a new note
@login_required
def note_add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(user=request.user, title=title, content=content)
        return redirect('note_list')
    return render(request, 'tasks/note_form.html')

# 3. Edit a note
@login_required
def note_edit(request):
    # (Logic for editing goes here - similar to task_edit)
    pass

# 4. Delete a note
@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return redirect('note_list')