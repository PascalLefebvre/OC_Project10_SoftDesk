from rest_framework import generics

from .models import Project
from .serializers import ProjectSerializer


class ListProject(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
