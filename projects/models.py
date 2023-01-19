from django.conf import settings
from django.db import models


class Project(models.Model):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.title[:30]} / {self.id}"


class Contributor(models.Model):

    AUTHOR = "AUTHOR"
    CONTRIBUTOR = "CONTRIBUTOR"

    ROLE_CHOICES = (
        (AUTHOR, "Auteur"),
        (CONTRIBUTOR, "Collaborateur"),
    )

    user_id = models.IntegerField()
    project_id = models.IntegerField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name="Rôle")

    class Meta:
        unique_together = ("user_id", "project_id")

    def __str__(self) -> str:
        return f"{self.user_id} / {self.project_id} / {self.role}"


class Issue(models.Model):

    ROLE_CHOICES_PRIORITY = (
        ("FAIBLE", "Faible"),
        ("MOYENNE", "Moyenne"),
        ("ELEVEE", "Elevée"),
    )

    ROLE_CHOICES_STATUS = (
        ("AFAIRE", "A faire"),
        ("ENCOURS", "En cours"),
        ("TERMINE", "Terminé"),
    )

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=30)
    priority = models.CharField(
        max_length=30, choices=ROLE_CHOICES_PRIORITY, verbose_name="Priorité"
    )
    status = models.CharField(max_length=30, choices=ROLE_CHOICES_STATUS)
    # project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    project_id = models.IntegerField()
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="issue_author",
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=author,
        related_name="issue_assignee",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title[:50]


class Comment(models.Model):

    description = models.CharField(max_length=500)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description[:50]


# class Contributor(models.Model):

#     AUTHOR = "AUTHOR"
#     CONTRIBUTOR = "CONTRIBUTOR"

#     ROLE_CHOICES = (
#         (AUTHOR, "Auteur"),
#         (CONTRIBUTOR, "Collaborateur"),
#     )

#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     project = models.ForeignKey(
#         to=Project, on_delete=models.CASCADE, related_name="contributors"
#     )
#     role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name="Rôle")

#     class Meta:
#         unique_together = (
#             "user",
#             "project",
#         )

#     def __str__(self) -> str:
#         return f"{self.user.username} / {self.project.title[:50]} / {self.role}"
