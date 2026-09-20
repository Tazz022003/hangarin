from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Task, Category, Priority, SubTask, Note

@login_required
def dashboard(request):
    tasks = Task.objects.all().order_by("deadline")

    context = {
        "tasks": tasks,
        "total_tasks": Task.objects.count(),
        "completed_tasks": Task.objects.filter(status="Completed").count(),
        "pending_tasks": Task.objects.filter(status="Pending").count(),
        "categories": Category.objects.all(),
        "priorities": Priority.objects.all(),
    }

    return render(request, "tasks/dashboard.html", context)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    context = {
        "task": task,
        "subtasks": task.subtask_set.all(),
        "notes": task.note_set.all().order_by("-created_at"),
    }

    return render(request, "tasks/task_detail.html", context)


def add_task(request):
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        status = request.POST.get("status")
        category_id = request.POST.get("category")
        priority_id = request.POST.get("priority")

        if (
            title
            and description
            and deadline
            and status
            and category_id
            and priority_id
        ):
            deadline = datetime.fromisoformat(deadline)

            if timezone.is_naive(deadline):
                deadline = timezone.make_aware(deadline)

            Task.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                status=status,
                category_id=category_id,
                priority_id=priority_id,
            )

            return redirect("dashboard")

    context = {
        "categories": categories,
        "priorities": priorities,
        "status_choices": Task.STATUS_CHOICES,
    }

    return render(request, "tasks/add_task.html", context)

def tasks_list(request):
    status = request.GET.get("status")

    tasks = Task.objects.all().order_by("deadline")

    if status in ["Pending", "In Progress", "Completed"]:
        tasks = tasks.filter(status=status)

    context = {
        "tasks": tasks,
        "current_status": status,
    }

    return render(request, "tasks/tasks_list.html", context)

def categories_list(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }

    return render(
        request,
        "tasks/categories_list.html",
        context,
    )

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        status = request.POST.get("status")
        category_id = request.POST.get("category")
        priority_id = request.POST.get("priority")

        if (
            title
            and description
            and deadline
            and status
            and category_id
            and priority_id
        ):
            deadline = datetime.fromisoformat(deadline)

            if timezone.is_naive(deadline):
                deadline = timezone.make_aware(deadline)

            task.title = title
            task.description = description
            task.deadline = deadline
            task.status = status
            task.category_id = category_id
            task.priority_id = priority_id
            task.save()

            return redirect("task_detail", task_id=task.id)

    context = {
        "task": task,
        "categories": categories,
        "priorities": priorities,
        "status_choices": Task.STATUS_CHOICES,
    }

    return render(request, "tasks/edit_task.html", context)

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("tasks_list")

    context = {
        "task": task,
    }

    return render(request, "tasks/delete_task.html", context)


def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")

        if title and status:
            task.subtask_set.create(
                title=title,
                status=status,
            )

            return redirect("task_detail", task_id=task.id)

    context = {
        "task": task,
        "status_choices": Task.STATUS_CHOICES,
    }

    return render(request, "tasks/add_subtask.html", context)


def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")

        valid_statuses = [value for value, label in Task.STATUS_CHOICES]

        if title and status in valid_statuses:
            subtask.title = title
            subtask.status = status
            subtask.save()

            return redirect(
                "task_detail",
                task_id=subtask.parent_task.id,
            )

    context = {
        "subtask": subtask,
        "status_choices": Task.STATUS_CHOICES,
    }

    return render(
        request,
        "tasks/edit_subtask.html",
        context,
    )




def update_subtask_status(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        status = request.POST.get("status")

        valid_statuses = [value for value, label in Task.STATUS_CHOICES]

        if status in valid_statuses:
            subtask.status = status
            subtask.save()

        return redirect("task_detail", task_id=subtask.parent_task.id)

    return redirect("task_detail", task_id=subtask.parent_task.id)

def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    task_id = subtask.parent_task.id

    if request.method == "POST":
        subtask.delete()
        return redirect("task_detail", task_id=task_id)

    context = {
        "subtask": subtask,
    }

    return render(
        request,
        "tasks/delete_subtask.html",
        context,
    )

def add_note(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Note.objects.create(
                task=task,
                content=content,
            )

            return redirect("task_detail", task_id=task.id)

    context = {
        "task": task,
    }

    return render(
        request,
        "tasks/add_note.html",
        context,
    )

def profile(request):
    return render(request, "tasks/profile.html")