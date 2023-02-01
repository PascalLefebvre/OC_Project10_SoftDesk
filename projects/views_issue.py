from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Contributor, Issue
from .serializers import IssueListSerializer, IssueDetailSerializer
from .permissions import IsProjectAuthor, IsProjectContributor


class IssueList(generics.ListCreateAPIView):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [
        IsAuthenticated & (IsProjectContributor | IsProjectAuthor),
    ]

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


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    pass
