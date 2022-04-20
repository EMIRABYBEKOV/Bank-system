from django.db import models
from account.models import Account
from django.utils.crypto import get_random_string
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from account.serializers import AccountSerializer
from django.db.models import Q
currencies = (
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('KGS', 'KGZ'),
)


class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    wallet_currency = models.CharField(max_length=3, choices=currencies, default='KGZ')
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

class TransferManager(models.Manager):
    def search(self, query, field):
        if field == 'trans_num':
            return Transfer.objects.filter(transfer_code=int(query))
        elif field == 'username':
            account = Account.objects.filter(username=query)
            if account.exists():
                account = Account.objects.get(username=query).pk
                return Transfer.objects.filter(Q(sender=account) | Q(receiver=account))
        return Credit.objects.none()

def transfer_code():
    code = get_random_string(length=10, allowed_chars='1234567890')
    return code

class Transfer(models.Model):
    transfer_code = models.IntegerField(default=transfer_code)
    sender = models.IntegerField()
    receiver = models.IntegerField()
    sum = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=currencies)

def send(transfer_code, sender, receiver, sum, currency):
    if receiver == currency:
        return {"message": "You can't do Transfer to yourself"}
    account = Account.objects.filter(pk=sender)
    if account.exists():
        transfer = Transfer(
            transfer_code=transfer_code,
            sender=sender,
            receiver=receiver,
            sum=sum,
            currency=currency
        )
        transfer.save()
        return {
            "Status": "Success",
            "Data": {
                "transfer_code": f"{transfer_code}",
                "sender": f"{sender}",
                "receiver": f"{receiver}",
                "sum": f"{sum}",
                "currency": f"{currency}",
            }
            }
    return {"message": f"We didn't find an Account with indentify number {sender}"}


credit_choices = (
    ('mortgage', 'mortgage'),
    ('consumer', 'consumer'),
)


def count_credit(user, salary, pledge, price, paid, j_check):
    if pledge == "consumer" and 300 <= price < 1000 and salary >= 100:  # without confidence
        final_amount = price + (price / 100) * 5
        month = int(final_amount / 12)

    elif pledge == "consumer" and 300 <= price < 1000 and salary >= 70:  # without confidence
        final_amount = price + (price / 100) * 6
        month = int(final_amount / 50)

    elif pledge == "consumer" and 1000 <= price < 10000 and salary >= 100 \
            and user.confidence:
        final_amount = price + (price / 100) * 9
        month = int(final_amount / 80)

    elif pledge == "consumer" and 10000 <= price <= 10000 and salary >= 500 \
            and user.confidence:
        final_amount = price + (price / 100) * 10
        month = int(final_amount / 400)

    elif pledge == "mortgage" and 10000 <= price < 100000 and paid >= (
            price / 100) * 30 and salary >= 1500:  # without confidence
        final_amount = price + (price / 100) * 20
        month = int((final_amount - paid) / 1500)

    elif pledge == "mortgage" and 100000 <= price <= 1000000 and paid >= (price / 100) * 40 and salary >= 5000 \
            and user.confidence:
        final_amount = price + (price / 100) * 25
        month = int((final_amount - paid) / 4000)

    date_payment = datetime.today() + relativedelta(months=month)
    credit_long = datetime(1, 1, 1) + relativedelta(months=month) - relativedelta(months=12, days=1)
    every_month = (final_amount - paid) / month
    if j_check is False:
        Credit.objects.save(user, salary, pledge, price, paid, final_amount, date_payment, credit_long, every_month)
    return {
        "user": user.pk,
        "salary": salary,
        "pledge": pledge,
        "price": price,
        "paid": paid,
        "final_amount": final_amount,
        "date_payment": date_payment.strftime('%Y-%m-%d'),
        "credit_long": credit_long.strftime('%Y-%m-%d'),
        "every_month": int(every_month),
    }


class CreditManager(models.Manager):
    def save(self, user, salary, pledge, price, paid, final_amount, date_payment, credit_long, every_month):

        credit = self.model(
                user=user,
                salary=salary,
                pledge=pledge,
                price=price,
                final_amount=final_amount,
                paid=paid,
                date_payment=date_payment.strftime('%Y-%m-%d'),
                credit_long=credit_long.strftime('%Y-%m-%d'),
                every_month=every_month,

            )

        credit.save(using=self._db)

    def search(self, query, field):
        if field == 'iden_num':
            return Credit.objects.filter(identification_number=int(query))
        elif field == 'username':
            account = Account.objects.filter(username=query)
            if account.exists():
                account = Account.objects.get(username=query).pk
                return Credit.objects.filter(user=account)
        return Credit.objects.none()




class Credit(models.Model):
    identification_number = models.IntegerField(default=transfer_code)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    salary = models.PositiveIntegerField()

    pledge = models.CharField(choices=credit_choices, null=True, blank=True, max_length=20) #залог

    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_long = models.DateField()
    date_taking = models.DateField(auto_now_add=True)

    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_payment = models.DateField()
    every_month = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    notices = models.IntegerField(default=0)
    
    approval = models.BooleanField(default=False)

    objects = CreditManager()

    def __str__(self):
        return f"{self.user}"





