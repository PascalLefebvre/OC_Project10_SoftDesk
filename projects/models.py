from django.conf import settings
from django.db import models


class Project(models.Model):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title[:30]


class Contributor(models.Model):

    CREATOR = "CREATOR"
    CONTRIBUTOR = "CONTRIBUTOR"

    ROLE_CHOICES = (
        (CREATOR, "Créateur"),
        (CONTRIBUTOR, "Collaborateur"),
    )

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name="Rôle")

    def __str__(self) -> str:
        return f"{self.user.username} / {self.project.title[:50]}"


class Issue(models.Model):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=30)
    priority = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_author",
    )
    assignee_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=author_user,
        related_name="issue_assignee",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title[:50]


class Comment(models.Model):

    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description[:50]
