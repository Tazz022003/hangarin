from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Task, Note, SubTask, Priority, Category


class Command(BaseCommand):
    help = "Generate fake data for Hangarin"

    def handle(self, *args, **kwargs):
        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities:
            self.stdout.write(
                self.style.ERROR("Please add Priority records first.")
            )
            return

        if not categories:
            self.stdout.write(
                self.style.ERROR("Please add Category records first.")
            )
            return

        statuses = ["Pending", "In Progress", "Completed"]

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=statuses),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                priority=fake.random_element(elements=priorities),
                category=fake.random_element(elements=categories),
            )

            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

            for _ in range(3):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=5),
                    status=fake.random_element(elements=statuses),
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully generated fake Tasks, Notes, and SubTasks."
            )
        )