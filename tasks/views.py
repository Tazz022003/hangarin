from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CategoryForm, NoteForm, SubTaskForm, TaskForm, PriorityForm
from .models import Category, Note, Priority, SubTask, Task


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/dashboard.html"
    ordering = ["deadline"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.count()
        context["completed_tasks"] = Task.objects.filter(status="Completed").count()
        context["pending_tasks"] = Task.objects.filter(status="Pending").count()
        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()
        return context


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/tasks_list.html"
    paginate_by = 5

    def get_ordering(self):
        allowed = [
            "deadline", "-deadline",
            "title", "-title",
            "status", "-status",
            "priority__name", "-priority__name",
            "category__name", "-category__name",
        ]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "deadline"

    def get_queryset(self):
        qs = super().get_queryset()

        status = self.request.GET.get("status")
        category_id = self.request.GET.get("category")
        priority_id = self.request.GET.get("priority")
        query = self.request.GET.get("q")

        valid_statuses = [value for value, label in Task.STATUS_CHOICES]
        if status in valid_statuses:
            qs = qs.filter(status=status)

        if category_id:
            qs = qs.filter(category_id=category_id)

        if priority_id:
            qs = qs.filter(priority_id=priority_id)

        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

        return qs.order_by(self.get_ordering())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status")
        context["current_category"] = self.request.GET.get("category")
        context["current_priority"] = self.request.GET.get("priority")
        context["query"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort_by", "deadline")
        return context
    
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        allowed_sorts = ["title", "-title", "status", "-status"]
        subtask_sort = self.request.GET.get("subtask_sort", "title")
        if subtask_sort not in allowed_sorts:
            subtask_sort = "title"

        subtask_query = self.request.GET.get("subtask_q", "")

        subtasks_qs = self.object.subtask_set.all()
        if subtask_query:
            subtasks_qs = subtasks_qs.filter(title__icontains=subtask_query)
        subtasks_qs = subtasks_qs.order_by(subtask_sort)

        paginator = Paginator(subtasks_qs, 5)
        subtasks_page = paginator.get_page(self.request.GET.get("subtask_page"))

        context["subtasks"] = subtasks_page
        context["subtask_sort"] = subtask_sort
        context["subtask_query"] = subtask_query

        context["notes"] = self.object.note_set.all().order_by("-created_at")
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/add_task.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()
        context["status_choices"] = Task.STATUS_CHOICES
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/edit_task.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["priorities"] = Priority.objects.all()
        context["status_choices"] = Task.STATUS_CHOICES
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"
    success_url = reverse_lazy("tasks_list")



# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------

class CategoriesListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = "categories"
    template_name = "tasks/categories_list.html"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "tasks/add_category.html"
    success_url = reverse_lazy("categories_list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "tasks/edit_category.html"
    context_object_name = "category"
    success_url = reverse_lazy("categories_list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "tasks/delete_category.html"
    context_object_name = "category"
    success_url = reverse_lazy("categories_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_count"] = Task.objects.filter(category=self.object).count()
        return context


# ---------------------------------------------------------------------------
# SubTask (nested under a Task)
# ---------------------------------------------------------------------------

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "tasks/add_subtask.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs["task_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent_task = self.task
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.task
        context["status_choices"] = Task.STATUS_CHOICES
        return context

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.task.id})


class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "tasks/edit_subtask.html"
    context_object_name = "subtask"
    pk_url_kwarg = "subtask_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.STATUS_CHOICES
        return context

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.object.parent_task.id})


class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = "tasks/delete_subtask.html"
    context_object_name = "subtask"
    pk_url_kwarg = "subtask_id"

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.object.parent_task.id})


class UpdateSubTaskStatusView(LoginRequiredMixin, View):
    """Quick toggle button on the task detail page — not a full CRUD view."""

    def post(self, request, subtask_id):
        subtask = get_object_or_404(SubTask, id=subtask_id)
        status = request.POST.get("status")
        valid_statuses = [value for value, label in Task.STATUS_CHOICES]

        if status in valid_statuses:
            subtask.status = status
            subtask.save()

        return redirect("task_detail", task_id=subtask.parent_task.id)


# ---------------------------------------------------------------------------
# Note (nested under a Task, inline only — no standalone list view)
# ---------------------------------------------------------------------------

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "tasks/add_note.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs["task_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.task
        return context

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.task.id})

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "tasks/edit_note.html"
    context_object_name = "note"
    pk_url_kwarg = "note_id"

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.object.task.id})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "tasks/delete_note.html"
    context_object_name = "note"
    pk_url_kwarg = "note_id"

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"task_id": self.object.task.id})


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/profile.html"


# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------

class PrioritiesListView(LoginRequiredMixin, ListView):
    ...

# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------

class PrioritiesListView(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = "priorities"
    template_name = "tasks/priorities_list.html"


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "tasks/add_priority.html"
    success_url = reverse_lazy("priorities_list")


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "tasks/edit_priority.html"
    context_object_name = "priority"
    success_url = reverse_lazy("priorities_list")


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = "tasks/delete_priority.html"
    context_object_name = "priority"
    success_url = reverse_lazy("priorities_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_count"] = Task.objects.filter(priority=self.object).count()
        return context