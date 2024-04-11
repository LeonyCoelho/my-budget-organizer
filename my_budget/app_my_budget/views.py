from django.shortcuts import render
from app_my_budget.models import Account

def home(request):
    accounts = Account.objects.all()
    context = {
        'accounts':accounts,
    }
    return render(request, 'home.html', context)