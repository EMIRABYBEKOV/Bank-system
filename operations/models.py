from django.db import models
from account.models import Account
from django.utils.crypto import get_random_string

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


# class CreditManager(models.Manager):
#     def save(self, user, salary, pledge, confidence, amount, paid, date_taking, date_payment):
#         # if user.
#         credit = self.model(
#             user=user,
#             salary=salary,
#             pledge=pledge,
#             confidence=confidence,
#             amount=amount,
#             paid=paid,
#             date_taking=date_taking,
#             date_payment=date_payment,
#                         )
#
#         credit.save(using=self._db)


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

    # objects = CreditManager()

    def __str__(self):
        return f"{self.user}"





