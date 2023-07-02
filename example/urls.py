"""URL configuration for example project."""

from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("task/", views.task_add_view, name="task"),
    path("auth/", include("django.contrib.auth.urls")),
]
