"""URL configuration for example project."""

from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("delay/", views.delay_view, name="delay"),
    path("auth/", include("django.contrib.auth.urls")),
]
