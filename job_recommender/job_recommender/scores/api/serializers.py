from rest_framework import serializers

from ..models import CompanySimilarity


class CompanySimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySimilarity
        fields = ["source_id", "target_id", "similarity", "formula"]