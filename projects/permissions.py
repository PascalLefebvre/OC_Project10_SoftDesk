from rest_framework import permissions

from .models import Project


class IsAuthor(permissions.BasePermission):
    """Permission to check if the authenticated user is the author of the object."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsProjectAuthor(permissions.BasePermission):
    """Permission to check if the authenticated user is the author of the project."""

    message = "You're not allowed because you're not the author of the project."

    def has_permission(self, request, view):
        project_id = view.kwargs["project_id"]
        if Project.objects.filter(
            id=project_id,
            contributors__user=request.user,
            contributors__role="AUTHOR",
        ).exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsIssueAuthor(IsAuthor):
    """Permission to check if the authenticated user is the author of the issue."""

    message = "You're not allowed because you're not the author of the issue."


class IsCommentAuthor(IsAuthor):
    """Permission to check if the authenticated user is the author of the comment."""

    message = "You're not allowed because you're not the author of the comment."


class IsProjectContributor(permissions.BasePermission):
    """Permission to check if the authenticated user is a contributor of the project."""

    message = "You're not allowed because you're not a contributor of the project."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
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


class IsCreator(permissions.BasePermission):
    """Permission to check if the authenticated user can create an object (except a project)."""

    message = "You're not allowed because you're not a contributor of the project."

    def has_permission(self, request, view):
        if request.method == "POST":
            project_id = view.kwargs["project_id"]
            if Project.objects.filter(
                id=project_id,
                contributors__user=request.user,
            ).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
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
