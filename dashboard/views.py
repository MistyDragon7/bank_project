from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from core.models import Account, Loan, Transaction


@require_http_methods(["GET", "POST"])
@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Admin view: show all pending loans for review
        pending_loans = Loan.objects.filter(status='PENDING')
        return render(request, 'dashboard/admin_dashboard.html', {
            'pending_loans': pending_loans
        })

    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return render(request, 'dashboard/no_account.html')
    recent_transactions = Transaction.objects.filter(
        Q(from_account=account) | Q(to_account=account)
    ).order_by('-timestamp')[:5]

    return render(request, 'dashboard/dashboard.html', {
        'account': account,
        'transactions': recent_transactions
    })


from django.db import transaction
from django.contrib import messages


@require_POST
@login_required
def approve_loan(request, loan_id):
    if not request.user.is_superuser:
        return redirect('dashboard')

    loan = get_object_or_404(Loan, id=loan_id)

    if loan.status == 'APPROVED':
        messages.info(request, "Loan already approved.")
        return redirect('dashboard')

    with transaction.atomic():
        loan.status = 'APPROVED'
        loan.save()

        account = Account.objects.get(user=loan.user)
        account.balance += loan.amount
        account.save()

        Transaction.objects.create(
            from_account=None,  # could use a system account here
            to_account=account,
            amount=loan.amount,
            type='loan'
        )

    messages.success(request, f"Loan of {loan.amount} approved for {loan.user.username}.")
    return redirect('dashboard')


@require_POST
@login_required
def reject_loan(request, loan_id):
    if request.user.is_superuser:
        loan = get_object_or_404(Loan, id=loan_id)
        loan.status = 'REJECTED'
        loan.save()
    return redirect('dashboard')
