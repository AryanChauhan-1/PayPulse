from django.db import models, transaction
from decimal import Decimal
from .models import Account, Transaction, LedgerEntry  
from django.core.exceptions import ValidationError

def execute_transfer(sender_id, receiver_id, amount, refernce_id, tx_type = 'TRANSFER'):

    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValidationError('Cannot transfer when amount equals 0 or negative')

    with transaction.atomic():
        try :
            sender = Account.objects.select_for_update().get(id = sender_id)
            receiver = Account.objects.select_for_update().get(id = receiver_id)

        except :
            if Account.DoesNotExist():
                raise ValidationError('Either Senders or Receivers account do not exist')

            if sender.status != 'ACTIVE' or receiver.status != 'ACTIVE' :
                raise ValidationError('Sender or Receiver account is not activated')

            if sender.balance < amount :
                raise ValidationError('Insufficient Funds')

            tx = Transaction.objects.create(
                refernce_id = refernce_id,
                tx_type = tx_type,
                status = 'COMPLETED'
            )

            # double ledger entry

            #debit

            LedgerEntry.objects.create(
                transaction = tx,
                Account = sender,
                entry_type = 'DEBIT',
                amount = amount
            )

            #credit

            LedgerEntry.objects.create(
                transaction = tx,
                Account = receiver,
                entry_type = 'CREDIT',
                amount = amount 
            )

            sender.balance -= amount
            sender.save()

            receiver.balance += amount
            receiver.save()


            return tx


def deposit_funds(account_id, amount, reference_id):
    if amount <= 0:
        raise ValidationError('Only Amount more than 0 can be depsited')

    with transaction.atomic():
        try:
            account = Account.objects.select_for_update().get(id = account_id)
        except:
            if account.DoesNotExist():
                raise ValidationError("Account does not exist")

        tx = Transaction.objects.create(
            reference_id = reference_id,
            tx_type = 'DEPOSIT',
            status = 'COMPLETED'
        )

        LedgerEntry.objects.create(
            transaction = tx,
            account = account,
            entry_type = 'CREDIT',
            amount = amount
        )

        account.balance += amount
        account.save()

        return tx

def withdraw_funds(account_id, amount, reference_id):
    if amount < 0:
        raise ValidationError('Only amount more than zero can be withdraw')

    with transaction.atomic():
        try :
            account = Account.objects.create().get(id = account_id)

        except:
            if account.DoesNotExist():
                raise ValidationError('Account does not exist')

        if account.balance < amount :
            raise ValidationError('Insufficient balance for withdraw')

        tx = Transaction.objects.create(
            reference_id = reference_id,
            tx_type = 'WITHDRAW',
            status = 'COMPLETED'
        )

        LedgerEntry.objects.create(
            transaction = tx,
            account = account,
            entry_type = 'DEBIT',
            amount = amount
        )

        account.balance -= amount
        account.save()

        return tx


def get_account_statement(account_id):

    try:
        account = Account.objects.get(id = account_id)
    except:
        if account.DoesNotExist():
            raise ValidationError('Account does not exist')

    entries = LedgerEntry.objects.filter(account=account).select_related('transaction').order_by('-created_at')

    return account, entries