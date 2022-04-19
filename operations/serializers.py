from rest_framework import serializers
from .models import Wallet, Transfer, transfer_code, Credit
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

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
    j_check = serializers.BooleanField(default=False, write_only=True)
    class Meta:
        model = Credit
        fields = (
            'j_check',
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
            'every_month',
            'notices',
        )
        extra_kwargs = {
            'date_taking': {'read_only': True},
            'identification_number': {'read_only': True},
            'every_month': {'read_only': True},
            'date_payment': {'read_only': True},
            'final_amount': {'read_only': True},
            'notices': {'read_only': True},

        }

    def save(self):

        user = self.validated_data['user']
        salary = self.validated_data['salary']
        pledge = self.validated_data['pledge']
        price = self.validated_data['price']
        paid = self.validated_data['paid']

        if user.verification:

            if pledge == "mortgage" and 10000 <= price <= 100000 and paid >= (price / 100) * 30 and salary >= 1500:
                final_amount = price + (price / 100) * 20
                month = int((final_amount - paid) / 1500)

            elif pledge == "mortgage" and 100000 <= price <= 1000000 and paid >= (price / 100) * 40 and salary >= 5000\
                    and user.confidence:
                final_amount = price + (price / 100) * 25
                month = int((final_amount - paid) / 4000)

            elif pledge == "consumer" and 300 <= price <= 1000 and salary >= 100:   #without confidence
                final_amount = price + (price / 100) * 11
                month = int(final_amount / 12)

            elif pledge == "consumer" and 300 <= price <= 1000 and salary >= 100\
                    and user.confidence:
                final_amount = price + (price / 100) * 11
                month = int(final_amount / 12)

            elif pledge == "consumer" and 1000 <= price <= 10000 and salary >= 100\
                    and user.confidence:
                final_amount = price + (price / 100) * 11
                month = int(final_amount / 12)



            date_payment = datetime.today() + relativedelta(months=month)
            credit_long = datetime(1, 1, 1) + relativedelta(months=month) - relativedelta(months=12, days=1)
            every_month = (final_amount - paid) / month

            self.validated_data['final_amount'] = final_amount
            self.validated_data['date_payment'] = date_payment.strftime('%Y-%m-%d')
            self.validated_data['credit_long'] = credit_long.strftime('%Y-%m-%d')
            self.validated_data['every_month'] = every_month


            credit = Credit(
                user=self.validated_data['user'],
                salary=self.validated_data['salary'],
                pledge=self.validated_data['pledge'],
                price=self.validated_data['price'],
                final_amount=self.validated_data['final_amount'],
                paid=self.validated_data['paid'],
                date_payment=self.validated_data['date_payment'],
                credit_long=self.validated_data['credit_long'],
                every_month=self.validated_data['every_month'],

            )

            if self.validated_data['j_check'] is False:
                credit.save()
