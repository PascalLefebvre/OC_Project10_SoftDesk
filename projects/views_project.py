from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Project, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer

from .permissions import IsProjectAuthor, IsProjectContributor


class ProjectList(generics.ListCreateAPIView):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        project_id = response.data.get("id")
        contributor = Contributor()
        contributor.user = request.user
        contributor.project = Project.objects.get(pk=project_id)
        contributor.role = contributor.AUTHOR
        contributor.save()

        return response


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = "id"
    lookup_url_kwarg = "project_id"
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsProjectAuthor)]

    def get_queryset(self):
        auth_user = self.request.user
        project_id = self.kwargs["project_id"]
        project = get_object_or_404(Project, id=project_id)
        queryset = Project.objects.filter(id=project_id)
        if self.request.method == "GET":
            if not Project.objects.filter(
                contributors__user=auth_user, id=project_id
            ).exists():
                raise Http404
        elif self.request.method in ["PUT", "DELETE"]:
            if not Contributor.objects.filter(
                user=auth_user, project=project, role="AUTHOR"
            ).exists():
                raise Http404
        else:
            queryset = None

        return queryset
