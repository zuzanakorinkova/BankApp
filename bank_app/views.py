from django.shortcuts import render, reverse, get_object_or_404
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .models import Customer, Rank, Account, Ledger
from django.http import HttpResponse
from django.contrib import messages

# from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('bank_app:staff'))
    else:
        return HttpResponseRedirect(reverse('bank_app:customer'))


def customer_index(request):
    assert not request.user.is_staff, 'return to staff page'
    customer = request.user.customer
    context = {
        'customer': customer
    }
    return render(request, 'bank_app/customer_index.html', context)


def customer_account_details(request, account_pk):
    assert not request.user.is_staff, 'return to staff page'
    account = get_object_or_404(Account, user=request.user, pk=account_pk)
    context = {
        'account': account,
    }
    return render(request, 'bank_app/customer_account_details.html', context)


def customer_make_transfer(request):
    assert not request.user.is_staff, 'return to staff page'
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        from_account = get_object_or_404(
            Account, pk=request.POST['from_account'])
        to_account = get_object_or_404(Account, pk=request.POST['to_account'])
        text = request.POST['text']
        Ledger.transfer(amount, from_account, to_account, text)
        messages.success(request, 'Transfer successful')
        return HttpResponseRedirect(reverse('bank_app:customer_make_transfer'))

    context = {
        'customer_accounts': request.user.customer.accounts.filter(is_loan=False),
        'all_accounts': Account.objects.all(),
    }
    return render(request, 'bank_app/customer_make_transfer.html', context)


def staff_index(request):
    assert request.user.is_staff, 'return to customer page'
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        if password == confirm_password:
            Customer.create_customer(username, password, email, phone_number)
            messages.success(request, 'Customer created')
            return HttpResponseRedirect(reverse('bank_app:staff'))
    context = {
        'ranks': Rank.objects.all(),
        # .order_by('username')
        'all_customers': User.objects.filter(is_staff=False)
    }
    return render(request, 'bank_app/staff_index.html', context)


def staff_customer_details(request, customer_pk):
    assert request.user.is_staff, 'return to customer page'
    if request.method == "POST" and "name" in request.POST:
        name = request.POST['name']
        user = get_object_or_404(User, pk=customer_pk)
        Account.create_account(user, name)
        messages.success(request, 'Account created')
        return HttpResponseRedirect(reverse('bank_app:staff_customer_details', args=(customer_pk)))

    if request.method == 'POST' and 'rank' in request.POST:
        rank = get_object_or_404(Rank, pk=request.POST['rank'])
        customer = get_object_or_404(Customer, user=customer_pk)
        customer.rank = rank
        customer.save()

    customer = get_object_or_404(User, pk=customer_pk)
    context = {
        'ranks': Rank.objects.all(),
        'customer': customer,
    }

    return render(request, 'bank_app/staff_customer_details.html', context)
