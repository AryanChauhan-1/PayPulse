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