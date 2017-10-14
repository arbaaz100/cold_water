# -*- coding: utf-8 -*-
"""
Created on Sat May 13 07:08:35 2017

@author: ASUS-PC
"""
import sqlite3
import sys

connection = sqlite3.connect("C:/Users\ASUS-PC\Desktop\Miniproject\company1.db", timeout = 10)

cursor = connection.cursor()

def New_Customer():
    username = input("\nPlease Enter the username ")
    password = input("\nPlease Enter the password ")
    pin = int(input("\nPlease Enter the pin "))
    first_name = input("\nPlease Enter your First Name ")
    last_name = input("\nPlease Enter your Last Name ")
    gender = (input("\n Please Enter your Gender (M/F) ")).lower()
    birth_date = input("\n Please Enter your DOB (YYYY-MM-DD) ")
    acc_type = (input("\nPlease Enter your Account Type (Credit/Savings) ")).lower()
    bal = float(input("\nPlease Enter the amount you want to deposit (Minimum = Rs.0) "))
    if bal < 0:
        print("\n The Amount entered is Invalid \n")
        print("Try Again\n")
        New_Customer()
    else:
        addr = input("\n Please Enter your Address ")
        aa = cursor.execute("SELECT MAX(cust_id) from customer")
        x = aa.fetchall()
        cust_id = x[0][0]+1
        bb = cursor.execute("SELECT MAX(acc_no) from customer")
        y = bb.fetchall()
        acc_no = y[0][0]+1
        #cc = cursor.execute("SELECT date() from customer")
        #z = cc.fetchall()
        #acc_start1 = z[0][0]
        acc_start = 1995-1-1
        acc_end = 2024-12-31
        rr = cursor.execute("INSERT INTO customer (cust_id, acc_no,first_name,last_name, addr, gender, acc_start, acc_end, birth_date, acc_type, username, password, pin, bal) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(cust_id, acc_no,first_name,last_name, addr, gender,acc_start, acc_end, birth_date, acc_type, username, password, pin, bal))
        print("Success , Your account has been created \n")
        print("Your customer ID : ",cust_id)
        print("Your password : ",password)
        print("Your Pin : ",pin)
        
def avail_loan(cust_id,password,pin):
    amt = float(input("\nEnter the Amount for Loan "))
    rr = cursor.execute("SELECT bal from customer WHERE cust_id = (?)",(cust_id,))
    r = rr.fetchall()
    bal = r[0][0]
    if amt <=0:
        print("\n Amount entered is Invalid\n")
        print("\n Please Enter again")
        avail_loan(cust_id,password,pin)
    elif amt > 2*bal:
        print("\n Amount Entered cannot be disbursed due to your low account balance")
    else:
        term = int(input("\n Enter the Time in Months "))
        if term <= 0:
            print("\n Term entered is Invalid\n")
            avail_loan(cust_id,password,pin)
        else:
            print("\n The Bank offers you an interest rate of 12.0% per annum on your amount\n")
            new_amt = amt + (amt*9.25*(term/12)/100)
            print("\n The Amount you have to pay after your Term:  Rs.",new_amt)
            print("\n The decided amount will be credited to your account ")
            x = (input("\n Are you sure (Y/N)")).lower()
            if x == 'n':
                print("Returning to Main Menu \n")
                main()
            elif x == 'y':
                
                bb = cursor.execute("SELECT MAX(loan_no) from loan")
                y = bb.fetchall()
                loan_no = y[0][0]+1
                
                cc = cursor.execute("SELECT MAX(Pay_id) from loan")
                z = cc.fetchall()
                Pay_id = z[0][0]+1
                
                rr  = cursor.execute("UPDATE customer SET bal = bal+(?) WHERE cust_id = (?);",(amt,cust_id))
                print("\nThe decided amount has been credited to your account\n")
                aa = cursor.execute("INSERT INTO loan(loan_no,Pay_id,cust_id,amt,term) VALUES (?,?,?,?,?)",(loan_no, Pay_id,cust_id, amt, term))
                print("Success\n","Your Loan ID  ",loan_no)
                print("Your Payment ID ",Pay_id)
            else:
                print("Invalid Choice , Enter Again")
                avail_loan(cust_id,password,pin)

def fixed_deposit(cust_id,password,pin):
    amt = float(input("\n Enter the Amount for Fixed Deposit "))
    rr = cursor.execute("SELECT bal from customer WHERE cust_id = (?)",(cust_id,))
    r = rr.fetchall()
    r = r[0][0]
    if amt <= 0:
        print("\n Amount entered is Invalid\n")
        print("\n Please Enter again")
        fixed_deposit(cust_id,password,pin)
    elif amt < 1000:
        print("\n Amount is less than minimum threshold i.e., Rs.1000")
        print("\n Please Enter again")
        fixed_deposit(cust_id,password,pin)
    elif amt > r:
        print("\n Not Sufficient Funds in Account ")
        fixed_deposit(cust_id,password,pin)
    else:
        term = int(input("\n Enter the Time in Months "))
        if term <= 0:
            print("\n Term entered is Invalid\n")
        elif term < 12:
            print("Term is less than Minimum Term i.e., 12 months ")
            print("\n Please Enter again")
            fixed_deposit(cust_id,password,pin)
        else:
            print("\n The Bank offers you a rate of 9.25% per annum on your amount\n")
            new_amt = amt + (amt*9.25*(term/12)/100)
            print("\n This sum you will receive after your decided term  Rs.",new_amt)
            print("\n The decided amount will be deducted from your account ")
            x = (input("\n Are you sure (Y/N)")).lower()
            if x == 'n':
                main()
            elif x == 'y':
                
                bb = cursor.execute("SELECT MAX(FD_no) from fixed_dep")
                y = bb.fetchall()
                FD_no = y[0][0]+1
                
                cc = cursor.execute("SELECT MAX(Pay_id) from fixed_dep")
                z = cc.fetchall()
                Pay_id = z[0][0]+1
                
                rr  = cursor.execute("UPDATE customer SET bal = bal-(?) WHERE cust_id = (?);",(amt,cust_id))
                print("\nThe decided amount has been deducted from your account\n")
                aa = cursor.execute("INSERT INTO fixed_dep(FD_no, Pay_id, cust_id, amt, term) VALUES (?,?,?,?,?)",(FD_no, Pay_id,cust_id, amt, term))
                print("Success\n","Your FD_id ",FD_no)
                print("Your Payment ID ",Pay_id)
            else:
                print("Invalid Choice , Enter Again")
                fixed_deposit(cust_id,password,pin)
                

def history(data):
    data = data[0]
    cust_id = data[0]
    acc_no = data[1]
    rr = cursor.execute("insert into history (cust_id, acc_no,close_date) values (?,?,date())",(cust_id,acc_no))
        
def admin_login():
    username = input("Enter the admin_id ")
    password = input("Enter the password ")
    if username == "group14" and password == "123":
        print("\n1.Check Closed Accounts History ")
        print("\n2.FD Report of a Customer ")
        print("\n3.FD Report of a Customer vis-a-vis another Customer ")
        print("\n4.FD Report wrt to a Particular FD Amount ")
        print("\n5.Loan Report of a Customer ")
        print("\n6.Loan Report of a Customer vis-a-vis another Customer ")
        print("\n7.Loan Report wrt to a Particular Loan Amount ")
        print("\n8.Loan-FD Report of a Customer ")
        print("\n9.Report of Customers who are yet to avail a Loan ")
        print("\n10.Report of Customers who are yet to open an FD Account ")
        print("\n11.FD Report of a Customers who neither have Loan nor have an FD account with the Bank ")
        print("\n0.Logout\n")
        choice = int(input())
        if choice == 1:
            print("\nThe following data about closed accounts\n")
            rr = cursor.execute("select * from history")
            data = rr.fetchall()
            for i in range(len(data)):
                print("\nCustomer ID : ",data[i][0])
                print("\nAccount Number : ",data[i][1])
                print("\nAccount Deletion Date : ",data[i][2])
            admin_login()
        elif choice == 0:
            main()
        elif choice == 2:
            cust_id = int(input("\nEnter the cust_id of the Customer : "))
            rr = cursor.execute("SELECT * FROM fixed_dep WHERE cust_id = (?);",(cust_id,))
            data = rr.fetchall()
            
            if len(list(data))==0:
                print("\n NA ")
                print("\n Customer Id Doesn't Exist or this Customer does not have any FD")
                admin_login()
            else:
                print("\n Numbers of FD of required Customer : ",len(data))
                for i in range(len(data)):
                    print("\nFD Account Number : ",data[i][0])
                    print("\nPayment ID : ",data[i][1])
                    print("Customer ID : ",data[i][2])
                    print("\nFD Amount :",data[i][3])
                    print("\nFD Term :", data[i][4]," Months")
                    print("\n")
                admin_login()
        elif choice == 3:
            cust_id = int(input("\nEnter the cust_id of the Customer"))
            rr = cursor.execute("select * from  fixed_dep where cust_id = (?)",(cust_id,))
            data = rr.fetchall()
            if len(data) == 0:
                print("Invalid Customer Id\n")
                admin_login()
            else:
                rb = cursor.execute("select * from fixed_dep where amt >( SELECT Sum(amt) FROM fixed_dep where cust_id = (?))",(cust_id,))
                data1 = rb.fetchall()
                data1 = list(data1[0])
                print("\nFD Account Number : ",data1[0])
                print("\nPayment ID : ",data1[1])
                print("\nFD Amount : ",data1[2])
                print("\nFD Term :", data1[3]," Months")
                print("\n")
                
        elif choice == 4:
            amt = float(input("\nEnter the Amount : "))
            if amt <=0:
                print("Invalid Amount, Enter Again \n")
                admin_login()
            elif (amt % 1000) != 0:
                print("Invalid Amount, Enter Again \n")
                admin_login()
            else:
                rr = cursor.execute("SELECT * FROM fixed_dep where amt>(?)",(amt,))
                data = rr.fetchall()
                for i in range(len(data)):
                    print("\nFD Account Number : ",data[i][0])
                    print("\nPayment ID : ",data[i][1])
                    print("\nCustomer ID : ",data[i][2])
                    print("\nFD Amount : ", data[i][3])
                    print("\n FD Term : ", data[i][4],"Months")
                    print("\n")
                    
        elif choice == 5:
            cust_id = int(input("\nEnter the cust_id of the Customer : "))
            rr = cursor.execute("SELECT * FROM loan WHERE cust_id = (?);",(cust_id,))
            data = rr.fetchall()
            
            if len(list(data))==0:
                print("\n NA ")
                print("\n Customer Id Doesn't Exist or this Customer does not have any Loan Pending ")
                admin_login()
            else:
                print("\n Numbers of Loans of required Customer : ",len(data))
                for i in range(len(data)):
                    print("\nLoan Account Number : ",data[i][0])
                    print("\nPayment ID : ",data[i][1])
                    print("Customer ID : ",data[i][2])
                    print("\nLoan Amount :",data[i][3])
                    print("\nLoan Term :", data[i][4]," Months")
                    print("\n")
                admin_login()
            
        elif choice == 6:
            cust_id = int(input("\nEnter the cust_id of the Customer"))
            rr = cursor.execute("select * from  loan where cust_id = (?)",(cust_id,))
            data = rr.fetchall()
            if len(data) == 0:
                print("Invalid Customer Id\n")
                admin_login()
            else:
                rb = cursor.execute("select * from loan where amt >( SELECT Sum(amt) FROM loan where cust_id = (?))",(cust_id,))
                data1 = rb.fetchall()
                if len(data1) == 0:
                    print("NA")
                else:
                    for i in range(len(data1)):
                        print("\nLoan Account Number : ",data1[i][0])
                        print("\nPayment ID : ",data1[i][1])
                        print("\nCustomer ID : ",data1[i][2])
                        print("\nLoan Amount : ",data1[i][3])
                        print("\nLoan Term :", data1[i][4]," Months")
                        print("\n")
                
        elif choice == 7:
            amt = float(input("\nEnter the Amount : "))
            if amt <=0:
                print("Invalid Amount, Enter Again \n")
                admin_login()
            elif (amt % 1000) != 0:
                print("Invalid Amount, Enter Again \n")
                admin_login()
            else:
                rr = cursor.execute("SELECT * FROM loan where amt>=(?)",(amt,))
                data = rr.fetchall()
                for i in range(len(data)):
                    print("\nLoan Account Number : ",data[i][0])
                    print("\nPayment ID : ",data[i][1])
                    print("\nCustomer ID : ",data[i][2])
                    print("\nLoan Amount : ", data[i][3])
                    print("\nLoan Term : ", data[i][4],"Months")
                    print("\n")
                    
        elif choice == 8:
            print("Still in developing stage \n")
                    
        elif choice == 9:
            rr = cursor.execute("SELECT cust_id FROM customer EXCEPT SELECT cust_id FROM loan")
            data = rr.fetchall()
            for i in range(len(data)):
                rb = cursor.execute("SELECT first_name,last_name FROM customer where cust_id = (?)",(data[i][0],))
                data1 = rb.fetchall()
                for j in range(len(data1)):
                    print("\n Customer ID : ",data[i][0])
                    print("\n First Name : ",data1[j][0])
                    print("\n Last Name : ",data1[j][1])
                    
        elif choice == 10:
            rr = cursor.execute("SELECT cust_id FROM customer EXCEPT SELECT cust_id FROM fixed_dep")
            data = rr.fetchall()
            for i in range(len(data)):
                rb = cursor.execute("SELECT first_name,last_name FROM customer where cust_id = (?)",(data[i][0],))
                data1 = rb.fetchall()
                for j in range(len(data1)):
                    print("\n Customer ID : ",data[i][0])
                    print("\n First Name : ",data1[j][0])
                    print("\n Last Name : ",data1[j][1])
                    
        elif choice == 11:
            rr = cursor.execute("select cust_id from customer except select cust_id from loan intersect select cust_id from customer except select cust_id from fixed_dep")
            data = rr.fetchall()
            for i in range(len(data)):
                rb = cursor.execute("SELECT first_name,last_name FROM customer where cust_id = (?)",(data[i][0],))
                data1 = rb.fetchall()
                for j in range(len(data1)):
                    print("\n Customer ID : ",data[i][0])
                    print("\n First Name : ",data1[j][0])
                    print("\n Last Name : ",data1[j][1])
            
        else:
            print("\nInvalid Choice")
            admin_login()
            
    else:
        print("\nInvalid Username or Password\n")
        main()
        
    

def main():
    print("Welcome to Bank, We care for you\n")                                   
    prompt=int(input("""1. Sign Up (New Customer)\n"""+                                        
                        """2. Sign In (Existing Customer)\n""" + """3. Administrator Sign In\n""" + 
                                       """4. Quit\n"""))    
    if prompt==1:
        New_Customer()
    elif prompt==2:
        cust_id = int(input("Customer ID:\n"))
        password = input("Password:\n")
        pin = int(input("Pin:\n"))
        Existing_Customer(cust_id,password,pin)
    elif prompt==3:
        admin_login()                    
    elif prompt==4:
        sys.exit()
    else:
        print("You have pressed the wrong key, please try again")
    
                               
def Addr_Change(cust_id,password,pin):
    address = str(input("Enter the New Address:"))
    rr  = cursor.execute("UPDATE customer SET addr = (?) WHERE cust_id = (?);",(address,cust_id))
    print("\nYour Address has been Successfully Updated\n")
    #Existing_Customer(cust_id,password,pin)
        
def Money_Deposit(cust_id,password,pin):
    amt = float(input("\nEnter the Amount to Deposit in your account :\n"))
    rr  = cursor.execute("UPDATE customer SET bal = bal+(?) WHERE cust_id = (?);",(amt,cust_id))
    print("\nThe sum has been deposited into your account\n") 
    #Existing_Customer(cust_id,password,pin)
   
def Money_Withdrawal(cust_id,password,pin):
    amt = float(input("\nEnter the Amount you want to Withdraw :\n"))
    if type(amt) == str:
        print("\n Invalid Amount Entered \n")
        Money_Withdrawal(cust_id,password,pin)
    elif amt < 0:
        print("\n Invalid Amount Entered \n")
        Money_Withdrawal(cust_id,password,pin)
    else:
        rb = cursor.execute("select bal from customer where cust_id = (?)",(cust_id,))
        data = rb.fetchall()
        bal = data[0][0]
        if amt > bal:
            print("\n Not Enough Funds in Savings \n")
        else:
            rr  = cursor.execute("UPDATE customer SET bal = bal-(?) WHERE cust_id = (?);",(amt,cust_id))
            print("\nThe sum has been withdrawal from your account\n")
        
def Transfer_money(cust_id,password,pin):
    acc = int(input("\nEnter the Account Number: \n"))
    amt = float(input("\nEnter the Amount you want to deposit in this account:\n"))
    xx  = cursor.execute("UPDATE customer SET bal = bal+(?) WHERE acc_no = (?);",(amt,acc))
    rr  = cursor.execute("UPDATE customer SET bal = bal-(?) WHERE cust_id = (?);",(amt,cust_id))
    print("\nThe Requested amount has been transferred to the beneficiary\n")
    #Existing_Customer(cust_id,password,pin)
    
def Account_closure(cust_id,password,pin):
    xx = cursor.execute("SELECT cust_id,acc_no from customer WHERE cust_id = (?) and password = (?);",(cust_id,password))
    data = xx.fetchall()
    x = input("\nDo you really want to close your account(Y/N)\n").lower()
    if x == 'y':
        rr  = cursor.execute("DELETE from customer WHERE cust_id = (?) and password = (?);",(cust_id,password))
        print("\nYour Account has been Closed\n")
        history(data)
    elif x == 'n':
        print("Action Aborted \n")
        main()
    else:
        print("Invalid Choice \n")
        
def Logout(cust_id,password):
    x = input("\nDo you want to Logout (Y/N) \n")
    x = x.lower()
    if x=='y':
        print("\nYou have been successfully logged out\n")
        main()

def Existing_Customer(cust_id,password,pin):  
    rr = cursor.execute("SELECT * FROM customer WHERE customer.cust_id = (?) and customer.password = (?) and customer.pin = (?);", (cust_id,password,pin))
    data = rr.fetchall() 
    if len(data)==0:
        print("Invalid Customer ID or Password or Wrong Pin")
    
    else:
        for i in data:
            print("\nYour Information")
            print("\nCustomer ID : ",i[0])
            print("\nAccount Number : ",i[1])
            print("\nName : ",i[2]+" "+i[3])
            print("\nAddress : ",i[4])
            if i[5]=='m':
                print("\nGender : Male ")
            else:
                print("\nGender : Female")
            print("\nAccount Start Date : ",i[6])
            print("\nAccount End Date : ",i[7])
            print("\nDate Of Birth : ",i[8])
            print("\nAccount Type : ",i[9])
            print("\nAvailable Balance : ",i[13])
            
            
        print("\n1. Address Change\n")
        print("\n2.Open New Account \n")
        print("\n3. Money Deposit\n")
        print("\n4. Money Withdrawal\n")
        print("\n5. Print Statement\n")
        print("\n6. Transfer Money\n")
        print("\n7. Account Closure\n")
        print("\n8. Avail Loan\n")
        print("\n0. Customer Logout\n")
        
        choice = int(input())
        if choice == 1:
            Addr_Change(cust_id,password,pin)
        elif choice == 2:
            print("\n Open New Account \n")
            x = int(input("""1. Open SA\n"""+                                        
                        """2. Open CA\n""" + """3. Open FD\n"""))   
            
            if x == 1:
                print("\nStill in Developing Stage\n")
            elif x == 2:
                print("\nStill in Developing Stage\n")
            elif x == 3:
                fixed_deposit(cust_id,password,pin)
            else:
                print("\nInvalid Choice \n")
                main()
            
        elif choice == 3:
            Money_Deposit(cust_id,password,pin)
        elif choice == 4:
            Money_Withdrawal(cust_id,password,pin)
        elif choice == 5:
            print("\nStill in Developing Stage\n")
        elif choice == 6:
            Transfer_money(cust_id,password,pin)
        elif choice == 7:
            Account_closure(cust_id,password,pin)
        elif choice == 8:
            avail_loan(cust_id,password,pin)
        elif choice == 0:
            Logout(cust_id,password)
        else:
            print("Wrong Choice!!!")

  
if __name__ == "__main__":
    main()
    
# never forget this, if you want the changes to be saved:

connection.commit()

connection.close()
