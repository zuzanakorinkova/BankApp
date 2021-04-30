from django.db import models, transaction
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.models import User
from uuid import uuid4
from django.conf import settings


class Rank(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField(unique=True)

    @classmethod
    def default_rank(cls):
        min_rank = cls.objects.all().aggregate(
            models.Min('value'))['value__min']
        return cls.objects.get(value=min_rank)

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    @classmethod
    def create_customer(cls, username, password, email, phone_number, rank=Rank.default_rank()):
        user = User.objects.create_user(
            username=username, password=password, email=email)
        cls(user=user, rank=rank, phone_number=phone_number).save()
        Account(user=user, name='Default Account').save()
        return user

    @property
    def accounts(self):
        return Account.objects.filter(user=self.user)

    @property
    def can_make_loan(self):
        if self.rank.name == 'Basic':
            return False
        else:
            return True

    def __str__(self):
        return f"{self.user} - {self.rank} - {self.phone_number} - {self.pk}"


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=35, unique=False)
    is_loan = models.BooleanField(default=False)

    @classmethod
    def create_account(cls, user, name):
        cls(user=user, name=name).save()

    @property
    def balance(self):
        return Ledger.objects.filter(account=self.pk).aggregate(models.Sum('amount'))['amount__sum'] or Decimal('0')

    @property
    def movements(self):
        return Ledger.objects.filter(account=self.pk)

    def __str__(self):
        return f"{self.pk} - {self.user} - {self.name}"


class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=35)

    @classmethod
    def transfer(cls, amount, from_account, to_account, text):
        with transaction.atomic():
            if not from_account.is_loan:
                transaction_id = str(uuid4())
                cls(account=from_account, transaction_id=transaction_id,
                    amount=-amount, text=text).save()
                cls(account=to_account, transaction_id=transaction_id,
                    amount=amount, text=text).save()
            else:
                print('cannot make transfer')

    def __str__(self):
        return f'{self.amount} - {self.transaction_id} - {self.account} - {self.text}'
