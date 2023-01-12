from django.urls import path

from .views import ListProject

urlpatterns = [
    path("", ListProject.as_view(), name="project_list"),
]
