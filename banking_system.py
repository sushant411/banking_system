#vedant gawari
#javeed sayyed
#sushant kshirsagar
#soham deshmane

from datetime import datetime

balance = 0
account_no = ""
name = ""
pin = ""
transaction_history = []   


loan_amount = 0
monthly_income = 0


last_receipt = None


BANK_OPEN_HOUR = 10     
BANK_CLOSE_HOUR = 16    
LUNCH_START_HOUR = 13   
LUNCH_END_HOUR = 14    


BANK_NAME = "SecureTrust Bank"
BANK_ADDRESS = "Talegoan Dhamdhere, pune 412208"
BANK_EMAIL = "support@securetrustbank.com"
BANK_CUSTOMER_CARE_CALL = "1800-123-4567 (Toll Free)"
BANK_CUSTOMER_CARE_SMS = "Send 'HELP' to 56767"


def print_bank_details():
    print("\n========== BANK DETAILS ==========")
    print(f"Bank Name        : {BANK_NAME}")
    print(f"Address          : {BANK_ADDRESS}")
    print(f"Email            : {BANK_EMAIL}")
    print("-----------------------------------")
    print("Customer Service")
    print(f"  Call           : {BANK_CUSTOMER_CARE_CALL}")
    print(f"  SMS            : {BANK_CUSTOMER_CARE_SMS}")
    print("===================================")


def is_bank_open(now=None):
    """
    Checks whether the bank is open for branch transactions
    (Deposit, Withdraw, Loan Apply/Repay).
    Returns (True, "") if open, else (False, "reason").

    `now` can be passed manually for testing; defaults to current time.
    """
    if now is None:
        now = datetime.now()

    if now.weekday() >= 5:
        return False, "Bank is CLOSED today (Saturday & Sunday are holidays)."

    if now.hour < BANK_OPEN_HOUR or now.hour >= BANK_CLOSE_HOUR:
        return False, f"Bank is closed. Working hours: {BANK_OPEN_HOUR}:00 to {BANK_CLOSE_HOUR}:00 (Mon-Fri)."

    if LUNCH_START_HOUR <= now.hour < LUNCH_END_HOUR:
        return False, f"Bank is closed for lunch break ({LUNCH_START_HOUR}:00 - {LUNCH_END_HOUR}:00). Please try later."

    return True, ""


def print_bank_timings():
    print("\n========== BANK TIMINGS ==========")
    print(f"Working Hours : {BANK_OPEN_HOUR}:00 - {BANK_CLOSE_HOUR}:00 (Monday to Friday)")
    print(f"Lunch Break   : {LUNCH_START_HOUR}:00 - {LUNCH_END_HOUR}:00")
    print("Weekly Off    : Saturday & Sunday")
    print("===================================")
    print("Note: UPI Payments work 24x7, even when the branch is closed,")
    print("      just like real UPI apps.")


def print_receipt(transaction, amount, extra_info=""):
    global last_receipt

    lines = []
    lines.append("====================================")
    lines.append("          BANK RECEIPT")
    lines.append("====================================")
    lines.append(f"Account Number : {account_no}")
    lines.append(f"Account Holder : {name}")
    lines.append(f"Transaction    : {transaction}")
    if extra_info:
        lines.append(extra_info)
    lines.append(f"Amount         : ₹{amount}")
    lines.append(f"Balance        : ₹{balance}")
    lines.append(f"Date/Time      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("====================================")
    lines.append("       Transaction Successful!")
    lines.append("====================================")

    receipt_text = "\n".join(lines)
    print("\n" + receipt_text)

    last_receipt = receipt_text   


def log_transaction(transaction, amount):
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": transaction,
        "amount": amount,
        "balance": balance
    }
    transaction_history.append(record)


def verify_pin():
    entered_pin = input("Enter your 4-digit PIN: ")
    if entered_pin == pin:
        return True
    else:
        print("Incorrect PIN! Transaction cancelled.")
        return False


def check_loan_eligibility(requested_amount, income):
    global loan_amount

    if loan_amount > 0:
        return False, "You already have an active loan. Repay it before applying again."
    if income <= 0:
        return False, "Monthly income must be greater than ₹0."
    if requested_amount <= 0:
        return False, "Loan amount must be greater than ₹0."

    max_eligible = income * 5
    if requested_amount > max_eligible:
        return False, f"Requested amount exceeds your eligibility limit of ₹{max_eligible:.2f} (5x income)."
    if requested_amount > 500000:
        return False, "Requested amount exceeds the maximum loan cap of ₹5,00,000."

    return True, ""


while True:

    print("\n========== BANKING SYSTEM ==========")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. UPI Payment")             
    print("5. Check Balance")
    print("6. Account Details")
    print("7. Transaction History")
    print("8. Bank Statement")          
    print("9. Apply for Loan")
    print("10. Repay Loan")
    print("11. View Last Receipt")
    print("12. Bank Timings")
    print("13. Bank Details")           
    print("14. Exit")
    print("====================================")

    choice = input("Enter your choice: ")

    
    if choice == "1":

        account_no = input("Enter Account Number: ")
        name = input("Enter Your Name: ")
        pin = input("Create 4 Digit PIN: ")

        if len(pin) == 4 and pin.isdigit():
            print("\nAccount Created Successfully!")
            print("Account Number:", account_no)
            print("Account Holder:", name)
        else:
            print("Invalid PIN!")
            print("PIN must contain exactly 4 digits.")
            account_no = ""
            pin = ""

   
    elif choice == "2":

        if account_no == "":
            print("Please create an account first.")
        else:
            open_now, reason = is_bank_open()
            if not open_now:
                print("\n", reason)
            else:
                try:
                    amount = float(input("Enter Deposit Amount: ₹"))
                    if amount > 0:
                        balance = balance + amount
                        print_receipt("DEPOSIT", amount)
                        log_transaction("DEPOSIT", amount)
                    else:
                        print("Invalid Amount!")
                except ValueError:
                    print("Please enter a valid number.")

    
    elif choice == "3":

        if account_no == "":
            print("Please create an account first.")
        else:
            open_now, reason = is_bank_open()
            if not open_now:
                print("\n", reason)
            elif not verify_pin():
                pass
            else:
                try:
                    amount = float(input("Enter Withdrawal Amount: ₹"))
                    if amount <= 0:
                        print("Invalid Amount!")
                    elif amount > balance:
                        print("Insufficient Balance!")
                    else:
                        balance = balance - amount
                        print_receipt("WITHDRAW", amount)
                        log_transaction("WITHDRAW", amount)
                except ValueError:
                    print("Please enter a valid number.")
    
    elif choice == "4":

        if account_no == "":
            print("Please create an account first.")
        elif not verify_pin():
            pass
        else:
            upi_id = input("Enter Recipient UPI ID (e.g. name@bank): ").strip()

            if "@" not in upi_id:
                print("Invalid UPI ID format. It should look like 'name@bank'.")
            else:
                try:
                    amount = float(input("Enter Amount to Pay: ₹"))
                    if amount <= 0:
                        print("Invalid Amount!")
                    elif amount > balance:
                        print("Insufficient Balance!")
                    else:
                        balance = balance - amount
                        print_receipt("UPI PAYMENT", amount, extra_info=f"Paid To      : {upi_id}")
                        log_transaction(f"UPI to {upi_id}", amount)
                except ValueError:
                    print("Please enter a valid number.")
    
    elif choice == "5":

        if account_no == "":
            print("Please create an account first.")
        else:
            print("\nYour Current Balance: ₹", balance)
    
    elif choice == "6":

        if account_no == "":
            print("Please create an account first.")
        else:
            print("\n========== ACCOUNT DETAILS ==========")
            print("Account Number :", account_no)
            print("Account Holder :", name)
            print("Balance        : ₹", balance)
            if loan_amount > 0:
                print("Active Loan    : ₹", loan_amount)

    elif choice == "7":

        if account_no == "":
            print("Please create an account first.")
        elif len(transaction_history) == 0:
            print("\nNo transactions yet.")
        else:
            print("\n========== TRANSACTION HISTORY ==========")
            for record in transaction_history:
                print(f"[{record['timestamp']}] {record['type']:<20} ₹{record['amount']:.2f}  | Balance after: ₹{record['balance']:.2f}")
            print("===========================================")

    
    elif choice == "8":

        if account_no == "":
            print("Please create an account first.")
        else:
            print("\n============================================================")
            print("                     BANK STATEMENT")
            print("============================================================")
            print(f"Account Number : {account_no}")
            print(f"Account Holder : {name}")
            print(f"Generated On   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("------------------------------------------------------------")
            print(f"{'Date/Time':<20}{'Type':<20}{'Amount':>10}   {'Balance':>10}")
            print("------------------------------------------------------------")

            if len(transaction_history) == 0:
                print("No transactions to display.")
            else:
                for record in transaction_history:
                    print(f"{record['timestamp']:<20}{record['type']:<20}{record['amount']:>10.2f}   {record['balance']:>10.2f}")

            print("------------------------------------------------------------")
            print(f"Closing Balance: ₹{balance:.2f}")
            if loan_amount > 0:
                print(f"Outstanding Loan: ₹{loan_amount:.2f}")
            print("============================================================")

    elif choice == "9":

        if account_no == "":
            print("Please create an account first.")
        else:
            open_now, reason = is_bank_open()
            if not open_now:
                print("\n", reason)
            elif not verify_pin():
                pass
            else:
                try:
                    requested_amount = float(input("Enter Loan Amount Requested: ₹"))
                    income = float(input("Enter Your Monthly Income: ₹"))

                    eligible, reject_reason = check_loan_eligibility(requested_amount, income)

                    if eligible:
                        loan_amount = requested_amount
                        monthly_income = income
                        balance = balance + requested_amount
                        print("\n Loan Approved!")
                        print_receipt("LOAN CREDIT", requested_amount)
                        log_transaction("LOAN CREDIT", requested_amount)
                    else:
                        print("\n Loan Application Rejected.")
                        print("Reason:", reject_reason)
                except ValueError:
                    print("Please enter valid numeric values.")
    
    elif choice == "10":

        if account_no == "":
            print("Please create an account first.")
        elif loan_amount <= 0:
            print("You have no active loan to repay.")
        else:
            open_now, reason = is_bank_open()
            if not open_now:
                print("\n", reason)
            elif not verify_pin():
                pass
            else:
                try:
                    repay_amount = float(input(f"Outstanding Loan: ₹{loan_amount:.2f}\nEnter Repayment Amount: ₹"))
                    if repay_amount <= 0:
                        print("Invalid Amount!")
                    elif repay_amount > balance:
                        print("Insufficient Balance to repay this amount!")
                    elif repay_amount > loan_amount:
                        print(f"Amount exceeds outstanding loan. Max repayable: ₹{loan_amount:.2f}")
                    else:
                        balance = balance - repay_amount
                        loan_amount = loan_amount - repay_amount
                        print_receipt("LOAN REPAYMENT", repay_amount)
                        log_transaction("LOAN REPAY", repay_amount)
                        if loan_amount == 0:
                            print(" Loan fully repaid!")
                        else:
                            print(f"Remaining Loan Balance: ₹{loan_amount:.2f}")
                except ValueError:
                    print("Please enter a valid number.")
    
    elif choice == "11":

        if account_no == "":
            print("Please create an account first.")
        elif last_receipt is None:
            print("No receipt available yet. Make a transaction first.")
        else:
            print("\n(Reprinting last receipt)")
            print(last_receipt)
   
    elif choice == "12":

        print_bank_timings()

    
    elif choice == "13":

        print_bank_details()

    
    elif choice == "14":

        print("\nThank you for using Banking System!")
        print("Have a nice day!")
        break
    
    else:

        print("Invalid Choice!")
        print("Please select a number from 1 to 14.")