from .models import Wallet
from .currency_parser import get_currency


def change_currency(user, value):
    wallet_model = Wallet.objects.get(user=user)
    if wallet_model.wallet_currency != value:
        if value == 'USD' and wallet_model.wallet_currency == 'EUR':
            num = int(wallet_model.wallet)
            num *= float(get_currency("EUR", "USD"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'USD'

        if value == 'EUR' and wallet_model.wallet_currency == 'USD':
            num = int(wallet_model.wallet)
            num *= float(get_currency("USD", "EUR"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'EUR'

        if value == 'KGS' and wallet_model.wallet_currency == 'USD':
            num = int(wallet_model.wallet)
            num *= float(get_currency("USD", "KGS"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'KGS'

        if value == 'KGS' and wallet_model.wallet_currency == 'EUR':
            num = int(wallet_model.wallet)
            num *= float(get_currency("EUR", "KGS"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'KGS'

        if value == 'EUR' and wallet_model.wallet_currency == 'KGS':
            num = int(wallet_model.wallet)
            num *= float(get_currency("KGS", "EUR"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'EUR'

        if value == 'USD' and str(wallet_model.wallet_currency) == 'KGS':
            num = int(wallet_model.wallet)
            num *= float(get_currency("KGS", "USD"))
            wallet_model.wallet = num
            wallet_model.wallet_currency = 'USD'

        wallet_model.save()

        return {'message': 'Successfully bought',
                'wallet': f'{wallet_model.wallet}'}
    return {'message': f"It's still in {value} currency"}