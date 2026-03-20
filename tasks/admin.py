from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task, SubTask, Category, Priority, Note

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(Note)