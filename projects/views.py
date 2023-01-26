from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Project, Contributor
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorListSerializer,
)
from .permissions import (
    IsProjectAuthor,
    IsProjectContributor,
)


class ProjectList(generics.ListCreateAPIView):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [
        IsAuthenticated,
    ]

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
    permission_classes = [
        IsAuthenticated & (IsProjectContributor | IsProjectAuthor),
    ]

    def get_queryset(self):
        auth_user = self.request.user
        project_id = self.kwargs["project_id"]
        if self.request.method == "GET":
            if not Project.objects.filter(
                contributors__user=auth_user, id=project_id
            ).exists():
                raise Http404
            queryset = Project.objects.filter(id=project_id)
        elif self.request.method in ["PUT", "DELETE"]:
            project = get_object_or_404(Project, id=project_id)
            if not Contributor.objects.filter(
                user=auth_user, project=project, role="AUTHOR"
            ).exists():
                raise Http404
            queryset = Project.objects.filter(id=project_id)
        else:
            queryset = None

        return queryset


class ContributorList(generics.ListCreateAPIView):

    lookup_field = "project"
    lookup_url_kwarg = "project_id"
    serializer_class = ContributorListSerializer
    permission_classes = [
        IsAuthenticated & (IsProjectContributor | IsProjectAuthor),
    ]

    def get_queryset(self):
        project = self.kwargs["project_id"]
        if not Contributor.objects.filter(
            project=project, user=self.request.user
        ).exists():
            raise Http404
        return Contributor.objects.filter(project=project)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        if self.request.method == "POST":
            draft_request_data = self.request.data.copy()
            draft_request_data["project"] = self.kwargs["project_id"]
            kwargs["data"] = draft_request_data

        return serializer_class(*args, **kwargs)


class ContributorDelete(generics.DestroyAPIView):

    lookup_field = "project"
    lookup_url_kwargs = ("user_id", "project_id")
    serializer_class = ContributorListSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectAuthor,
    ]

    def get_queryset(self):
        project = self.kwargs["project_id"]
        user = self.kwargs["user_id"]
        if not Contributor.objects.filter(
            project=project, user=self.request.user, role="AUTHOR"
        ).exists():
            raise Http404
        return Contributor.objects.filter(project=project, user=user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        for lookup_url_kwarg in self.lookup_url_kwargs:
            assert lookup_url_kwarg in self.kwargs, (
                "Expected view %s to be called with a URL keyword argument "
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                "attribute on the view correctly."
                % (self.__class__.__name__, lookup_url_kwarg)
            )

        filter_kwargs = {}
        for lookup_url_kwarg in self.lookup_url_kwargs:
            filter_kwargs[lookup_url_kwarg] = self.kwargs[lookup_url_kwarg]
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj
