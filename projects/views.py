from rest_framework import generics

from .models import Project, Contributor

from .serializers import ProjectListSerializer, ProjectDetailSerializer


class ProjectList(generics.ListCreateAPIView):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        queryset = []
        if self.request.method == "GET":
            queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset

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
        contributor.role = "CREATOR"
        contributor.save()

        return response


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        queryset = []
        user = self.request.user
        project_id = self.kwargs["pk"]
        if self.request.method == "GET":
            queryset = Project.objects.filter(contributors__user=user, id=project_id)
        elif self.request.method != "PATCH":
            queryset = Project.objects.filter(
                contributors__user=user, id=project_id, contributors__role="CREATOR"
            )
        return queryset
