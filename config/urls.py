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
    DashboardView,
    NoteCreateView,
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
    CategoryCreateView, 
    CategoryUpdateView, 
    CategoryDeleteView
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

    path("categories/", CategoriesListView.as_view(), name="categories_list"),

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

    path("tasks/<int:task_id>/notes/add/", NoteCreateView.as_view(), name="add_note"),

    # Add to the imports at the top:
# from tasks.views import CategoryCreateView, CategoryUpdateView, CategoryDeleteView

# Add these to urlpatterns, near the existing categories_list path:

    path("categories/add/", CategoryCreateView.as_view(), name="add_category"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="edit_category"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete_category"),
]