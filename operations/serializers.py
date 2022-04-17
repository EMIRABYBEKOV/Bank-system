from rest_framework import serializers
from .models import Wallet, Transfer, transfer_code, Credit
from rest_framework.validators import UniqueTogetherValidator


class WalletSerializer(serializers.ModelSerializer):
    wallet_currency = serializers.CharField(default='KGZ', read_only=True, write_only=False)

    class Meta:
        model = Wallet
        fields = (
            'user',
            'wallet_currency',
            'wallet',
            'is_active',
        )
        extra_kwargs = {
            'wallet': {'read_only': True},
            'is_active': {'read_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Wallet.objects.all(),
                fields=['user']
            )
        ]


currencies = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('KGS', 'KGZ'),
)

class ChangeCurrencySerializer(serializers.Serializer):
    currency = serializers.ChoiceField(choices=currencies)


class TransferSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(default=transfer_code, read_only=True)

    class Meta:
        model = Transfer
        fields = (
            'code',
            'sender',
            'receiver',
            'sum',
            'currency',
        )


class CreditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credit
        fields = (
            'identification_number',
            'user',
            'salary',
            'pledge',
            'price',
            'final_amount',
            'paid',
            'credit_long',
            'date_taking',
            'date_payment',
        )
        extra_kwargs = {
            'date_taking': {'read_only': True},
        }

    def save(self):
        credit = Credit(
            identification_number=self.validated_data['identification_number'],
            user=self.validated_data['user'],
            salary=self.validated_data['salary'],
            pledge=self.validated_data['pledge'],
            price=self.validated_data['price'],
            final_amount=self.validated_data['final_amount'],
            paid=99999,#self.validated_data['9999'],
            date_payment=self.validated_data['date_payment'],
            credit_long=self.validated_data['credit_long'],
        )

        credit.save()




