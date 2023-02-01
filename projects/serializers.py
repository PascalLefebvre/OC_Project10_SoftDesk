from rest_framework import serializers

from .models import Project, Contributor, Issue


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


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "status",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "project",
            "author",
            "assignee",
            "created_time",
        ]
