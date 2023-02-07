from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from .models import Project, Contributor, Comment
from .serializers import CommentListSerializer, CommentDetailSerializer
from .permissions import IsProjectContributor, IsCreator, IsCommentAuthor


class CommentList(generics.ListCreateAPIView):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsCreator)]

    def get_queryset(self):
        project = self.kwargs["project_id"]
        issue = self.kwargs["issue_id"]
        if not Contributor.objects.filter(
            project=project, user=self.request.user
        ).exists():
            raise Http404
        return Comment.objects.filter(issue=issue)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())

        # Update the kwargs dictionary with the necessary data to create the comment.
        if self.request.method == "POST":
            draft_request_data = self.request.data.copy()
            draft_request_data["author"] = self.request.user.id
            draft_request_data["issue"] = self.kwargs["issue_id"]
            kwargs["data"] = draft_request_data

        return serializer_class(*args, **kwargs)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = "id"
    lookup_url_kwarg = "comment_id"
    serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated & (IsProjectContributor | IsCommentAuthor)]

    def get_queryset(self):
        auth_user = self.request.user
        project_id = self.kwargs["project_id"]
        comment_id = self.kwargs["comment_id"]
        queryset = Comment.objects.filter(id=comment_id)

        if self.request.method == "GET":
            if not Project.objects.filter(
                contributors__user=auth_user, id=project_id
            ).exists():
                raise Http404
        elif self.request.method in ["PUT", "DELETE"]:
            if not Comment.objects.filter(author=self.request.user).exists():
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
            draft_request_data["issue"] = self.kwargs["issue_id"]
            kwargs["data"] = draft_request_data

        return serializer_class(*args, **kwargs)
