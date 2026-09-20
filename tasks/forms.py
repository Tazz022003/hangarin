from django import forms

from .models import Category, Note, SubTask, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline", "status", "category", "priority"]
        widgets = {
            "deadline": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title", "status"]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]