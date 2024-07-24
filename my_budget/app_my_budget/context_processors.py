from .models import GlobalSettings, Account, Transaction

def global_currency(request):
    global_settings = GlobalSettings.objects.first()
    currency = global_settings.currency if global_settings else 'BRL'  # Moeda padrão se não houver configurações globais

    accounts = Account.objects.all()
    transactions = Transaction.objects.all()

    for account in accounts:
        # Filtra as transações associadas a esta conta
        account_transactions = transactions.filter(account=account) | transactions.filter(target_account=account)

        # Calcula o total de receitas (income) para esta conta
        total_income_account = sum(transaction.amount for transaction in account_transactions if transaction.transaction_type == 'Income' and transaction.paid)

        # Calcula o total de despesas (expenses) para esta conta
        total_expenses_account = sum(transaction.amount for transaction in account_transactions if transaction.transaction_type == 'Expense' and transaction.paid)

        # Calcula o total de transferências recebidas (somar)
        total_transfer_in = sum(transaction.amount for transaction in account_transactions if transaction.transaction_type == 'Transfer' and transaction.target_account == account and transaction.paid)

        # Calcula o total de transferências enviadas (subtrair)
        total_transfer_out = sum(transaction.amount for transaction in account_transactions if transaction.transaction_type == 'Transfer' and transaction.account == account and transaction.paid)

        # Calcula o saldo total para esta conta
        account.total_balance = total_income_account - total_expenses_account + total_transfer_in - total_transfer_out

    # Recalcula os totais globais com a nova lógica
    total_income = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Income' and transaction.paid)
    total_expenses = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Expense' and transaction.paid)
    total_transfer_in = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Transfer' and transaction.target_account is not None and transaction.paid)
    total_transfer_out = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Transfer' and transaction.account is not None and transaction.paid)

    total_balance = total_income - total_expenses + total_transfer_in - total_transfer_out

    return {
        'global_currency': currency,
        'accounts': accounts,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_balance': total_balance,
        }
