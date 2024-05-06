from django.db import models

class GlobalSettings(models.Model):
    CURRENCY_CHOICES = [
        ('R$', 'Reais (BRL)'),
        ('$', 'US Dollar (USD)'),
    ]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BRL')

class Account(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_type_choices = [
        ('Savings', 'Savings'),
        ('Checking', 'Checking'),
        ('Investment', 'Investment'),
        ('Credit', 'Credit'),
    ]
    account_type = models.CharField(max_length=20, choices=account_type_choices)

    def __str__(self):
        return self.name

class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)

class TransactionSubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    picture = models.ImageField(upload_to='transaction_pictures/', blank=True, null=True)
    transaction_type_choices = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Transfer', 'Transfer'),
    ]
    transaction_type = models.CharField(max_length=20, choices=transaction_type_choices)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(TransactionSubCategory, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    target_account = models.ForeignKey(Account, related_name='transactions_received', on_delete=models.CASCADE, null=True, blank=True) # Permitindo que o campo seja nulo
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recurrent = models.BooleanField(default=False)
    paid = models.BooleanField(default=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'Transfer':
            self.category = None
            self.subcategory = None
        super().save(*args, **kwargs)


class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Budget(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
