from django.db import models
import users
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class Account(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, default='INR')

    balance = models.DecimalField(max_digits=12, decimal_places = 2, default = 0.00)
    
    class statuses(models.TextChoices):
        active = 'ACTIVE'
        not_active = 'NOT_ACTIVE'
       
    status = models.CharField(max_length = 10, choices = statuses.choices, default = 'ACTIVE')


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    reference_id = models.CharField(max_length = 100, unique=True)

    tx_type = models.CharField(max_length = 20)

    class tran_status(models.TextChoices):
        pending = 'PENDING'
        completed = 'COMPLETED'

    status = models.CharField(max_length = 20, choices = tran_status.choices, default = 'pending')
    created_at = models.DateTimeField(auto_now_add=True)


class LedgerEntry(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    class entry_types(models.TextChoices):
        debit = 'DEBIT', 'debit'
        credit = 'CREDIT', 'credit'

    entry_type = models.CharField(max_length = 10, choices=entry_types.choices)
    amount = models.DecimalField(max_digits=12, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add=True)
