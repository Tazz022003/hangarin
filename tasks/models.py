
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Note(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    def __str__(self):
        return self.content[:50]


class SubTask(BaseModel):
    parent_task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=Task.STATUS_CHOICES,
        default="Pending",
    )

    def __str__(self):
        return self.title
# Create your models here.
