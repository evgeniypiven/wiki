"""
Pages serializers
"""

# Standard library imports.

# Related third party imports.
from rest_framework import serializers
from reversion.models import Revision, Version
from django.utils import timezone

# Local application/library specific imports.
from .models import Page


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'text',
            'photo',
            'dt_created',
            'dt_updated',
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.dt_updated = timezone.now()

        instance.save()

        return instance


class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = (
            'id',
            'date_created',
            'user',
            'comment',
        )


class VersionSerializer(serializers.ModelSerializer):
    revision = RevisionSerializer()
    revision_obj_fields = serializers.SerializerMethodField(method_name='get_field_dict', required=False)

    def get_field_dict(self, obj):
        return PagesSerializer(obj.field_dict, many=False).data

    class Meta:
        model = Version
        fields = (
            'revision',
            'revision_obj_fields',
        )
