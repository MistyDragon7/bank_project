from django.contrib import admin
from .models import User, Account, Transaction, Loan
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Loan)