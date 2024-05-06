from django.shortcuts import render, redirect
from app_my_budget.models import Account, Transaction
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.db.models import F
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.contrib import messages





# def home(request):
#     accounts = Account.objects.all()
#     total_amount = sum(account.amount for account in accounts)
#     context = {
#         'accounts':accounts,
#         'total_amount': total_amount,
#     }
#     return render(request, 'home.html', context)

def home(request):
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    total_amount = sum(account.amount for account in accounts)

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'total_amount': total_amount,
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