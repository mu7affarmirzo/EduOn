from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class TransferSerializer(serializers.Serializer):
    number = serializers.CharField(required=False, allow_blank=True, max_length=100)
    expire = serializers.CharField(required=False, allow_blank=True, max_length=100)
    amount = serializers.IntegerField(required=False)
