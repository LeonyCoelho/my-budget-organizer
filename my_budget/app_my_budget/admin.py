from django.contrib import admin
from .models import GlobalSettings, Account, TransactionCategory, TransactionSubCategory, Transaction, Goal, Budget

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'account_type')
    search_fields = ('name', 'account_type')

@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(TransactionSubCategory)
class TransactionSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name', 'parent__name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'transaction_type', 'category', 'subcategory', 'account', 'amount', 'recurrent', 'paid', 'paid_at', 'due_at', 'created_at', 'updated_at')
    list_filter = ('transaction_type', 'category', 'account', 'recurrent', 'paid')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'target_amount', 'target_date', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'goal', 'category', 'amount', 'created_at', 'updated_at')
    list_filter = ('goal', 'category')
    search_fields = ('goal__name', 'category__name')
    date_hierarchy = 'created_at'
