from rest_framework import serializers

from .models import Project, Contributor


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
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


class ContributorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "user",
            "project",
            "role",
        ]
