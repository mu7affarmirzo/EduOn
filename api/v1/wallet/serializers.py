from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from wallet.models import CardModel


class TransferSerializer(serializers.Serializer):
    number = serializers.CharField(required=False, allow_blank=True, max_length=100)
    expire = serializers.CharField(required=False, allow_blank=True, max_length=100)
    amount = serializers.IntegerField(required=False)


class WalletHistorySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)


class CardSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_username_from_owner')

    class Meta:
        model = CardModel
        fields = [
            'card_number',
            'expire',
            'owner'
        ]

    def get_username_from_owner(self, card):
        owner = card.owner.phone_number
        return owner
