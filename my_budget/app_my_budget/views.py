from django.shortcuts import render, redirect
from app_my_budget.models import Account, Transaction
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET
from django.urls import reverse



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
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        transaction_type = request.POST.get('transaction_type')
        # Obtenha o ID da categoria, subcategoria e conta da transação do formulário (substitua com os valores reais)
        category_id = request.POST.get('category_id')
        subcategory_id = request.POST.get('subcategory_id')
        account_id = request.POST.get('account')
        amount = request.POST.get('amount')
        recurrent = request.POST.get('recurrent', False) == 'on'  # Converte a string 'on' para True
        paid = request.POST.get('paid', False) == 'on'  # Converte a string 'on' para True
        paid_at = request.POST.get('paid_at')
        due_at = request.POST.get('due_at')
        
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

    # Se não for uma requisição POST, apenas renderize a página inicial com as contas existentes
    context = {
        'accounts': accounts,
    }
    return render(request, 'home.html', context)