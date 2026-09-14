"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import UserLoginView
from tasks.views import (
    dashboard, 
    task_detail,
    add_task, 
    tasks_list, 
    edit_task, 
    delete_task, 
    add_subtask,  
    update_subtask_status, 
    edit_subtask,
    delete_subtask,
    add_note,
    categories_list,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", UserLoginView.as_view(), name="login"),
    path("", dashboard, name="dashboard"),
    path("tasks/add/", add_task, name="add_task"),
    path("tasks/", tasks_list, name="tasks_list"),
    path("categories/", categories_list, name="categories_list"),
    path("tasks/<int:task_id>/edit/", edit_task, name="edit_task"),
    path("tasks/<int:task_id>/delete/", delete_task, name="delete_task"),
    path( "tasks/<int:task_id>/subtasks/add/", add_subtask, name="add_subtask"),
    path( "tasks/<int:task_id>/notes/add/", add_note, name="add_note"),
    path( "subtasks/<int:subtask_id>/status/", update_subtask_status, name="update_subtask_status"),
    path( "subtasks/<int:subtask_id>/edit/", edit_subtask, name="edit_subtask"),
    path( "substasks/<int:subtask_id>/delete", delete_subtask, name="delete_subtask"),
    path("tasks/<int:task_id>/", task_detail, name="task_detail"),
]
