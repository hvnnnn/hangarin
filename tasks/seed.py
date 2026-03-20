from faker import Faker
from django.utils import timezone
import random

from .models import Task, SubTask, Note, Category, Priority

fake = Faker()

def run():
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    for _ in range(10):
        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            status=random.choice(["Pending", "In Progress", "Completed"]),
            deadline=timezone.make_aware(fake.date_time_this_month()),
            priority=random.choice(priorities),
            category=random.choice(categories),
        )

        # Create SubTasks
        for _ in range(3):
            SubTask.objects.create(
                task=task,
                title=fake.sentence(),
                status=random.choice(["Pending", "In Progress", "Completed"]),
            )

        # Create Notes
        for _ in range(2):
            Note.objects.create(
                task=task,
                content=fake.paragraph(),
            )