from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django.http import Http404
from django.db.models import Q

from .models import Project, Contributor, Issue
from .serializers import IssueListSerializer, IssueDetailSerializer
from .permissions import (
    IsProjectContributor,
    IsCreator,
    IsIssueAuthor,
    IsIssueAssignee,
)


class IssueList(generics.ListCreateAPIView):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsCreator)]

    def get_queryset(self):
        project = self.kwargs["project_id"]
        if not Contributor.objects.filter(
            project=project, user=self.request.user
        ).exists():
            raise Http404
        return Issue.objects.filter(project=project)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        if self.request.method == "POST":
            draft_request_data = self.request.data.copy()
            draft_request_data["author"] = self.request.user.id
            draft_request_data["project"] = self.kwargs["project_id"]
            kwargs["data"] = draft_request_data

        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        project = self.kwargs["project_id"]
        assignee = request.data["assignee"]
        if not Contributor.objects.filter(project=project, user=assignee).exists():
            raise ValidationError(
                {
                    "creation denied": "The assignee of the issue must be a contributor of the project."
                }
            )
        return super().create(request, *args, **kwargs)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = "id"
    lookup_url_kwarg = "issue_id"
    serializer_class = IssueDetailSerializer
    permission_classes = [
        IsAuthenticated & (IsProjectContributor | IsIssueAuthor | IsIssueAssignee)
    ]

    def get_queryset(self):
        auth_user = self.request.user
        project_id = self.kwargs["project_id"]
        issue_id = self.kwargs["issue_id"]
        queryset = Issue.objects.filter(id=issue_id)

        if self.request.method == "GET":
            if not Project.objects.filter(
                contributors__user=auth_user, id=project_id
            ).exists():
                raise Http404
        elif self.request.method == "PUT":
            if not Issue.objects.filter(
                Q(author=auth_user) | Q(assignee=auth_user) & Q(project__id=project_id)
            ).exists():
                raise Http404
        elif self.request.method == "DELETE":
            if not Issue.objects.filter(
                author=auth_user, project__id=project_id
            ).exists():
                raise Http404
        else:
            queryset = None

        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        if self.request.method == "PUT":
            draft_request_data = self.request.data.copy()
            draft_request_data["author"] = self.request.user.id
            draft_request_data["project"] = self.kwargs["project_id"]
            kwargs["data"] = draft_request_data

        return serializer_class(*args, **kwargs)
