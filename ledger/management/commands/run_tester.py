import uuid
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from ledger.services import ( execute_transfer, deposit_funds, withdraw_funds, get_account_statement)


class Command(BaseCommand) :
    help = 'Fintech Engine Tester'

    def handle(self, *args, **kwargs) :
        self.stdout.write(self.style.SUCCESS('----------  PayPulse Engine tester  ----------'))

        while True :
            self.stdout.write(self.style.WARNING('---  Main Menu  ---'))
            print('1. Transfer money')
            print('2. Deposit funds')
            print('3. Withdraw funds')
            print('4. Retrieve past statements')
            print('5. Exit Engine')

            choice = input(' Select one of the service (1 - 5) : ').strip()

            if choice == '1':
                self.run_transfer_Service()
            elif choice == '2':
                self.run_deposit_service()
            elif choice == '3' :
                self.run_withdraw_funds()
            elif choice == '4' :
                self.run_statement_service()
            elif choice == '5':
                self.stdout.write(self.style.SUCCESS('........ Exiting Terminal .......'))
                break
            else :
                self.stdout.write(self.style.ERROR('....... INVALID CHOICE___TRY AGAIN .......'))



    def generate_reference_id(self, prefix):
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
    
    def run_transfer_Service(self):
        self.stdout.write(self.style.SUCCESS('----- ENTERING FUNDS TRANSFER SERVICE -----'))
        sender_id = input("Enter the sender_id (UUID format) : ").strip()
        receiver_id = input("Enter the receiver_id (UUID format) : ").strip()
        amount = input("Enter amount to transfer : ").strip()

        try :
            tx = execute_transfer(sender_id, receiver_id, amount, self.generate_reference_id(), tx_type='TRANSFER')
            self.stdout.write(self.style.SUCCESS('----- Transfer Complete -----'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR('[FAILED] -- {e.message}'))
        except Exception as e:
            self.stdout.write(self.style.write("[SYSTEM ERROR] -- {str(e)}"))


    def run_deposit_service(self):
        self.stdout.write(self.style.SUCCESS('----- ENTERING DEPOSIT FUNDS SERVICE -----'))
        account_id = input("Enter Account_id to deposit funds into (UUID): ").strip()
        amount = input("Enter amount to deposit : ").strip()

        try:
            tx = deposit_funds(account_id, amount, self.generate_reference_id() )
            self.stdout.write(self.style.SUCCESS('----- Deposit Complete -----'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR('[FAILED] -- {e.message}'))
        except Exception as e:
            self.stdout.write(self.style.write("[SYSTEM ERROR] -- {str(e)}"))


    def run_withdraw_funds(self):
        self.stdout.write(self.style.SUCCESS('----- ENTERING WITHDRAW FUNDS SERVICE -----'))
        account_id = input("Enter Account_id to withdraw_funds from (UUID) : ").strip()
        amount = input("Enter amount to withdraw : ").strip()

        try:
            tx = self.run_withdraw_funds(account_id, amount, self.generate_reference_id())
            self.stdout.write(self.style.SUCCESS('----- Withdraw Complete -----'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR('[FAILED] -- {e.message}'))
        except Exception as e:
            self.stdout.write(self.style.write("[SYSTEM ERROR] -- {str(e)}"))


    def run_statement_service(self):
        self.stdout.write(self.style.SUCCESS('----- PRINTING ACCOUNT STATEMENT -----'))
        account_id = input('Enter account_id to print statement of (UUID) : ').strip()

        try :
            account, entries = get_account_statement(account_id)

            self.stdout.write(self.style.SUCCESS(f" Account Id : {account_id}"))
            self.stdout.write(self.style.SUCCESS(f" Account Holder : {account.user.email}"))
            self.stdout.write(self.style.SUCCESS(f" Account Id : {account_id}"))

            print(f"{'DATE' : < 25}  |  {'TYPE' : <10}  |  {'AMOUNT' : <10} |   {'REF_ID'}")
            print("-"*50)

            for entry in entries:
                date_str = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{date_str : <25}  |  {entry.entry_type : <10}  |  {entry.amount <10}  |  {entry.transaction.reference_id}")

        except ValidationError as e:
            self.stdout.write(self.style.ERROR("[FAILED] - {e.message}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR("[SYSTEM ERROR] - str(e)"))