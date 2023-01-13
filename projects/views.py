from rest_framework import generics

from .models import Project
from .serializers import ProjectSerializer


class ListProject(generics.ListAPIView):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(contributor__user=self.request.user)
        return queryset
