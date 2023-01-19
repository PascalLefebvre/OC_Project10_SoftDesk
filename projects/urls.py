from django.urls import path

from .views import ProjectList, ProjectDetail, ContributorList, ContributorDelete

urlpatterns = [
    path("", ProjectList.as_view(), name="project_list"),
    path("<int:project_id>/", ProjectDetail.as_view(), name="project_detail"),
    path("<int:project_id>/users/", ContributorList.as_view(), name="user_list"),
    path(
        "<int:project_id>/users/<int:user_id>/",
        ContributorDelete.as_view(),
        name="user_delete",
    ),
]
