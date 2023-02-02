from rest_framework import permissions

from .models import Project


class IsAuthor(permissions.BasePermission):
    """Permission to check if the authenticated user is an author."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsIssueAuthor(IsAuthor):
    """Permission to check if the authenticated user is the author of the issue."""

    message = "You're not allowed because you're not the author of the issue."


class IsCommentAuthor(IsAuthor):
    """Permission to check if the authenticated user is the author of the comment."""

    message = "You're not allowed because you're not the author of the comment."


class IsProjectAuthor(permissions.BasePermission):
    """Permission to check if the authenticated user is the author of the project."""

    message = "You're not allowed because you're not the author of the project."

    def is_project_author(self, request, view):
        project_id = view.kwargs["project_id"]
        if Project.objects.filter(
            id=project_id,
            contributors__user=request.user,
            contributors__role="AUTHOR",
        ).exists():
            return True
        return False

    def has_permission(self, request, view):
        return self.is_project_author(request, view)

    def has_object_permission(self, request, view, obj):
        return self.is_project_author(request, view)


class IsProjectContributor(permissions.BasePermission):
    """Permission to check if the authenticated user is a contributor of the project."""

    message = "You're not allowed because you're not a contributor of the project."

    def has_permission(self, request, view):
        methods = ("GET", "HEAD", "OPTIONS", "POST")
        if request.method in methods:
            project_id = view.kwargs["project_id"]
            if Project.objects.filter(
                id=project_id,
                contributors__user=request.user,
            ).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if Project.objects.filter(
                id=obj.id, contributors__user=request.user
            ).exists():
                return True
        return False


class IsIssueAssignee(permissions.BasePermission):
    """Permission to check if the authenticated user is the assignee of the issue."""

    message = "You're not allowed because you're not the assignee of the issue."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        methods = ("GET", "HEAD", "OPTIONS", "PUT")
        if request.method in methods:
            return obj.assignee == request.user
        return False
