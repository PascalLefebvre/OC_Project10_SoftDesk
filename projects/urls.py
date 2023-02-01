from django.urls import path

from .views_project import ProjectList, ProjectDetail
from .views_contributor import ContributorList, ContributorDelete
from .views_issue import IssueList, IssueDetail

urlpatterns = [
    path("", ProjectList.as_view(), name="project_list"),
    path("<int:project_id>/", ProjectDetail.as_view(), name="project_detail"),
    path("<int:project_id>/users/", ContributorList.as_view(), name="user_list"),
    path(
        "<int:project_id>/users/<int:user_id>/",
        ContributorDelete.as_view(),
        name="user_delete",
    ),
    path("<int:project_id>/issues/", IssueList.as_view(), name="issue_list"),
    path(
        "<int:project_id>/issues/<int:issue_id>/",
        IssueDetail.as_view(),
        name="issue_detail",
    ),
]
