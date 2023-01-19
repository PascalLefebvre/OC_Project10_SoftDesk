from rest_framework import serializers

from .models import Project, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "project_id",
            "user_id",
            "role",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
        ]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "user_id",
            "project_id",
            "role",
        ]
