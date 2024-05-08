from django.shortcuts import render, redirect
from app_my_budget.models import Account, Transaction
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import F, Sum, Q
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseBadRequest


# def home(request):
#     accounts = Account.objects.all()
#     transactions = Transaction.objects.all()
#     total_amount = sum(account.amount for account in accounts)

#     current_month = datetime.now().month
#     expenses_this_month = Transaction.objects.filter(
#         transaction_type='Expense',
#         paid=True,
#         paid_at__month=current_month
#     )
#     total_expenses = expenses_this_month.aggregate(Sum('amount'))['amount__sum'] or 0

#     context = {
#         'accounts': accounts,
#         'transactions': transactions,
#         'total_amount': total_amount,
#         'total_expenses': total_expenses,
#     }
#     return render(request, 'home.html', context)


# def home(request):
#     accounts = Account.objects.annotate(
#         total_amount=Sum('transaction__amount', filter=Q(transaction__paid=True))
#     )

#     transactions = Transaction.objects.all()

#     # Calcular o saldo total
#     total_amount = sum(account.total_amount for account in accounts if account.total_amount is not None)

#     # Calcular as despesas totais no mês atual
#     current_month = datetime.now().month
#     total_expenses = Transaction.objects.filter(
#         transaction_type='Expense',
#         paid=True,
#         paid_at__month=current_month
#     ).aggregate(Sum('amount'))['amount__sum'] or 0

#     context = {
#         'accounts': accounts,
#         'transactions': transactions,
#         'total_amount': total_amount,
#         'total_expenses': total_expenses,
#     }
#     return render(request, 'home.html', context)

def home(request):
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()

    # Calcula o total de receitas (income)
    total_income = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Income' if transaction.paid)

    # Calcula o total de despesas (expenses)
    total_expenses = sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Expense' if transaction.paid)

    # Calcula o saldo total subtraindo as despesas do total de receitas
    total_balance = total_income - total_expenses

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_balance': total_balance,
    }
    return render(request, 'home.html', context)


def new_transaction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        transaction_type = request.POST.get('transaction_type')
        category_id = request.POST.get('category_id')
        subcategory_id = request.POST.get('subcategory_id')
        account_id = request.POST.get('account')
        amount = request.POST.get('amount')
        recurrent = request.POST.get('recurrent', False) == 'on'
        paid = request.POST.get('paid', False) == 'on'
        paid_at = request.POST.get('paid_at')
        due_at = request.POST.get('due_at')

        # Converte o valor da quantia para um decimal
        amount = Decimal(amount)

        # Se 'paid_at' não estiver preenchido, use a data e hora atuais
        if not paid_at:
            paid_at = timezone.now()

        if not due_at:
            due_at = timezone.now()

        # Se 'due_at' não for obrigatório caso 'paid' seja True
        if not paid:
            # Se 'due_at' não estiver preenchido e 'paid' for False, retorne um erro
            if not due_at:
                return HttpResponseBadRequest("Due date is required for unpaid transactions.")

        # Adicionar ou subtrair o valor da transação ao saldo da conta correspondente
        if transaction_type == 'Income':
            Account.objects.filter(id=account_id).update(amount=F('amount') + amount)
        elif transaction_type == 'Expense':
            Account.objects.filter(id=account_id).update(amount=F('amount') - amount)

        # Crie e salve a nova transação no banco de dados
        new_transaction = Transaction.objects.create(
            name=name,
            description=description,
            transaction_type=transaction_type,
            category_id=category_id,
            subcategory_id=subcategory_id,
            account_id=account_id,
            amount=amount,
            recurrent=recurrent,
            paid=paid,
            paid_at=paid_at,
            due_at=due_at,
        )
        # Redirecione de volta para a página inicial após adicionar a transação
        return redirect('home')
    
def new_transfer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        transaction_type = 'transfer'
        category_id = None
        account_id = request.POST.get('account')
        target_account_id = request.POST.get('target_account')
        amount = request.POST.get('amount')
        paid = request.POST.get('paid', False) == 'on'
        paid_at = request.POST.get('paid_at')
        due_at = request.POST.get('due_at')

        # Verifique se as contas de origem e destino são diferentes
        if account_id == target_account_id:
            messages.error(request, 'A conta de origem e destino devem ser diferentes para realizar uma transferência.')
            return redirect('new_transfer')
        
        # Obtenha as instâncias das contas de origem e destino
        account = get_object_or_404(Account, id=account_id)
        target_account = get_object_or_404(Account, id=target_account_id)
        
        # Verifique se o saldo da conta de origem é suficiente para a transferência
        if account.amount < Decimal(amount):
            messages.error(request, 'O saldo da conta de origem é insuficiente para realizar esta transferência.')
            return redirect('new_transfer')
        # Crie e salve a nova transação no banco de dados
        new_transaction = Transaction.objects.create(
            name=name,
            description=description,
            transaction_type=transaction_type,
            category_id=category_id,
            account_id=account_id,
            target_account_id=target_account_id,
            amount=amount,
            paid=paid,
            paid_at=paid_at,
            due_at=due_at,
        )

        # Atualize os saldos das contas de origem e destino
        account.amount -= Decimal(amount)
        target_account.amount += Decimal(amount)
        account.save()
        target_account.save()

        # Redirecione de volta para a página inicial após adicionar a transação
        return redirect('home')
    
    else:
        # Se a requisição for GET, retorne um formulário vazio
        return redirect('home')
    
def new_account(request):
    if request.method == 'POST':
        # Coletando os dados do formulário
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        account_type = request.POST.get('account_type')

        # Criando uma nova instância de Account com os dados do formulário
        new_account = Account.objects.create(
            name=name,
            amount=amount,
            account_type=account_type
        )

        # Redirecionando para a página inicial após a criação da conta
        return redirect('home')

    # Se o método HTTP não for POST, renderize a página do modal novamente
    return render('home')
    
def delete_selected_accounts(request):
    if request.method == 'POST':
        selected_account_ids = request.POST.getlist('selected_accounts')
        # Exclua as contas selecionadas do banco de dados
        Account.objects.filter(id__in=selected_account_ids).delete()
    return redirect('home')  # Redireciona de volta para a página inicial após a exclusão