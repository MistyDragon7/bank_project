from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import RegisterForm, LoanForm
from .models import Account, Transaction


@login_required
def dashboard(request):
    # If the user is a superuser (admin), skip Account-related stuff
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')  # or wherever your admin-specific template is

    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return render(request, 'dashboard/no_account.html')  # or handle gracefully however you like

    return render(request, 'dashboard/dashboard.html', {'account': account})
def home(request):
    return render(request, 'home.html')

@login_required
def transfer_money(request):
    if request.method == 'POST':
        to_acc_no = request.POST['to_account']
        amount = Decimal(request.POST['amount'])
        from_account = Account.objects.get(user=request.user)
        try:
            to_account = Account.objects.get(account_number=to_acc_no)
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(from_account=from_account, to_account=to_account, amount=amount, type='transfer')
        except Account.DoesNotExist:
            return render(request, 'transfer.html', {'error': 'Invalid account number'})
        return redirect('dashboard')
    return render(request, 'transfer.html')

@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.save()
            return redirect('dashboard')
    else:
        form = LoanForm()
    return render(request, 'loan.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            acc_no = 'ACC' + str(user.id).zfill(6)
            Account.objects.create(user=user, account_number=acc_no, balance=1000.0)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})