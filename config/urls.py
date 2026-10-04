"""
URL configuration for config project.
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from accounts.views import signup
from tasks.views import (
    CategoriesListView,
    CategoryCreateView,
    CategoryDeleteView,
    CategoryUpdateView,
    DashboardView,
    NoteCreateView,
    NotesListView,
    StandaloneNoteCreateView,
    PrioritiesListView,
    PriorityCreateView,
    PriorityDeleteView,
    PriorityUpdateView,
    ProfileView,
    SubTaskCreateView,
    SubTaskDeleteView,
    SubTaskUpdateView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
    UpdateSubTaskStatusView,
    NoteUpdateView,
    NoteDeleteView,

)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "login/",
        RedirectView.as_view(pattern_name="account_login", query_string=True),
        name="login",
    ),
    path("accounts/", include("allauth.urls")),
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("tasks/", TaskListView.as_view(), name="tasks_list"),
    path("tasks/add/", TaskCreateView.as_view(), name="add_task"),
    path("tasks/<int:task_id>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:task_id>/edit/", TaskUpdateView.as_view(), name="edit_task"),
    path("tasks/<int:task_id>/delete/", TaskDeleteView.as_view(), name="delete_task"),

    path(
        "tasks/<int:task_id>/subtasks/add/",
        SubTaskCreateView.as_view(),
        name="add_subtask",
    ),
    path(
        "subtasks/<int:subtask_id>/edit/",
        SubTaskUpdateView.as_view(),
        name="edit_subtask",
    ),
    path(
        "subtasks/<int:subtask_id>/delete/",
        SubTaskDeleteView.as_view(),
        name="delete_subtask",
    ),
    path(
        "subtasks/<int:subtask_id>/status/",
        UpdateSubTaskStatusView.as_view(),
        name="update_subtask_status",
    ),

    path(
    "notes/add/",
    StandaloneNoteCreateView.as_view(),
    name="add_standalone_note",
),
path("notes/", NotesListView.as_view(), name="notes_list"),

    path("tasks/<int:task_id>/notes/add/", NoteCreateView.as_view(), name="add_note"),

    path("categories/", CategoriesListView.as_view(), name="categories_list"),
    path("categories/add/", CategoryCreateView.as_view(), name="add_category"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit_category"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete_category"),

    path("priorities/", PrioritiesListView.as_view(), name="priorities_list"),
    path("priorities/add/", PriorityCreateView.as_view(), name="add_priority"),
    path("priorities/<int:pk>/edit/", PriorityUpdateView.as_view(), name="edit_priority"),
    path("priorities/<int:pk>/delete/", PriorityDeleteView.as_view(), name="delete_priority"),
    #  NoteUpdateView, NoteDeleteView to the tasks.views import list

    path("notes/", NotesListView.as_view(), name="notes_list"),
    path("notes/<int:note_id>/edit/", NoteUpdateView.as_view(), name="edit_note"),
    path("notes/<int:note_id>/delete/", NoteDeleteView.as_view(), name="delete_note"),

    path('', include('pwa.urls')),
]   