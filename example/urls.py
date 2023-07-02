"""URL configuration for example project."""

from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("asgi/", views.aindex_view, name="aindex"),
    path("task/", views.task_add_view, name="task"),
    path("auth/", include("django.contrib.auth.urls")),
]
