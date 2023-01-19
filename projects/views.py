from rest_framework import generics, status
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Project, Contributor

from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorSerializer,
)


class ProjectList(generics.ListCreateAPIView):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Contributor.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        contributor = Contributor()
        contributor.user_id = request.user.id
        contributor.project_id = response.data.get("id")
        contributor.role = contributor.AUTHOR
        contributor.save()

        return response


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = "id"
    lookup_url_kwarg = "project_id"
    serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        project_id = self.kwargs["project_id"]
        if self.request.method == "GET":
            if not Contributor.objects.filter(
                user_id=user_id, project_id=project_id
            ).exists():
                raise Http404
            return Project.objects.filter(id=project_id)
        elif self.request.method != "PATCH":
            if not Contributor.objects.filter(
                user_id=user_id, project_id=project_id, role="AUTHOR"
            ).exists():
                raise Http404
            return Project.objects.filter(id=project_id)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        contributors = Contributor.objects.filter(project_id=project.id)
        for contributor in contributors:
            self.perform_destroy(contributor)

        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorList(generics.ListCreateAPIView):

    lookup_field = "project_id"
    lookup_url_kwarg = "project_id"
    serializer_class = ContributorSerializer
    # detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        project_id = self.kwargs["project_id"]
        if not Contributor.objects.filter(
            project_id=project_id, user_id=user_id
        ).exists():
            raise Http404
        return Contributor.objects.filter(project_id=project_id)

    # def get_serializer_class(self):
    #     if self.request.method == "POST":
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context.update(
    #         {
    #             "project": self.kwargs["pk"],
    #             "role": "CONTRIBUTOR",
    #         }
    #     )
    #     return context

    #     AssertionError: When a serializer is passed a `data` keyword argument you must call `.is_valid()` before attempting to access the serialized `.data` representation.
    # You should either call `.is_valid()` first, or access `.initial_data` instead.

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs["context"] = self.get_serializer_context()

    #     draft_request_data = self.request.data.copy()
    #     draft_request_data["project_id"] = self.kwargs["pk"]
    #     draft_request_data["role"] = "CONTRIBUTOR"
    #     kwargs["data"] = draft_request_data

    #     return serializer_class(*args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)

    #     project_id = self.kwargs["pk"]
    #     user_id = response.data.get("user_id")

    #     contributor = Contributor()
    #     contributor.user = request.user
    #     contributor.project = Project.objects.get(pk=project_id)
    #     contributor.role = contributor.AUTHOR
    #     contributor.save()

    #     return response


class ContributorDelete(generics.DestroyAPIView):

    lookup_url_kwargs = ("user_id", "project_id")
    serializer_class = ContributorSerializer

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        user_id = self.kwargs["user_id"]
        if not Contributor.objects.filter(
            project_id=project_id, user_id=self.request.user.id, role="AUTHOR"
        ).exists():
            raise Http404
        return Contributor.objects.filter(project_id=project_id, user_id=user_id)

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
