print("""
$$\   $$\  $$$$$$\  $$\    $$\ $$$$$$\ $$\   $$\        $$$$$$\  /$$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$$$\ 
$$ | $$  |$$  __$$\ $$ |   $$ |\_$$  _|$$$\  $$ |      $$  __$$\/__$$  __|$$  __$$\ $$  __$$\ $$  _____|
$$ |$$  / $$ /  $$ |$$ |   $$ |  $$ |  $$$$\ $$ |      $$ /  \__|  $$ |   $$ /  $$ |$$ |  $$ |$$ |      
$$$$$  /  $$$$$$$$ |\$$\  $$  |  $$ |  $$ $$\$$ |      \$$$$$$\    $$ |   $$ |  $$ |$$$$$$$  |$$$$$\    
$$  $$<   $$  __$$ | \$$\$$  /   $$ |  $$ \$$$$ |       \____$$\   $$ |   $$ |  $$ |$$  __$$< $$  __|   
$$ |\$$\  $$ |  $$ |  \$$$  /    $$ |  $$ |\$$$ |      $$\   $$ |  $$ |   $$ |  $$ |$$ |  $$ |$$ |      
$$ | \$$\ $$ |  $$ |   \$  /   $$$$$$\ $$ | \$$ |      \$$$$$$  |  $$ |    $$$$$$  |$$ |  $$ |$$$$$$$$\ 
\__|  \__|\__|  \__|    \_/    \______|\__|  \__|       \______/   \__|    \______/ \__|  \__|\________|                                                                                              
""")
print("""
 ____  __  __  _  _    _  _  _____  _    _    ____   __   _  _    __      __   ____  ____  ____ 
(  _ \(  )(  )( \/ )  ( \( )(  _  )( \/\/ )  (  _ \ /__\ ( \/ )  (  )    /__\ (_  _)( ___)(  _ \ 
 ) _ < )(__)(  \  /    )  (  )(_)(  )    (    )___//(__)\ \  /    )(__  /(__)\  )(   )__)  )   /
(____/(______) (__)   (_)\_)(_____)(__/\__)  (__) (__)(__)(__)   (____)(__)(__)(__) (____)(_)\_)   
                                    
""")


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="bnpl"
)

mycursor = mydb.cursor()

def numlen(n):
    return (len(str(n)))

def cid():
    sql = f"select max(customerid) from customers "
    mycursor.execute(sql)
    ID=mycursor.fetchall()
    if  ((ID[0])[0]) == None:
        x=0
        return x
    else:
        x=((ID[0])[0])
        return x



def numcheck(n):
    if numlen (n) == 10:
        return True
    else :
        return False

def biocheck(bio):
    if len(bio)==0:
        return False
    else:
        return True

def search(num):
    sql = f"SELECT * FROM customers WHERE MobNo = {num} "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    if biocheck(myresult):
        bio=[(myresult[0])[0],(myresult[0])[1],(myresult[0])[2],(myresult[0])[3],(myresult[0])[4],(myresult[0])[5]]
        return bio        
    else:
        bio=[]
        return bio

def addcust():
    print(':::::New CUstomer form:::::')
    c=True
    print(f'Customer ID: {(cid()+1)}')
    a=cid()+1
    while c:
        name=(input('Enter the Name(50char):')).upper()
        if name.isalpha() and len(name)<=50:
            b=name
            break
        else:
            print('Invalid customer Name !!Try again!!')
            continue    
    while c:
        num=(input('Enter the Mobile number:'))
        if num.isnumeric():
            if len(num)==10:
                if len(search(num))==0:
                  c=int(num)
                  break
                else:
                  c=False
                  print('Customer Already exists')
                  break
            else:
                print('Invalid Number !!Try again!!')
                continue
        else:
            print('Invalid Number !!Try again!!')
            continue
    while c:
        email=(input('Enter the Email address(100char):')).lower()
        x='@' 
        y='.com'
        if x and y in email and len(email)<=100:
            d=email
            break
        else:
            print('Invalid Email address !!Try again!!')
            continue    
    while c:
        addr=input('Enter the Address(150char):')
        if len(addr)<=150:
            break
        else:
            print('characters more than 150')
            continue
    while c:
        sql=f"INSERT INTO CUSTOMERS (CustomerID,Name,MobNo,Email,Address) values({a},'{b}',{c},'{d}','{addr}')"
        mycursor.execute(sql)
        mydb.commit()
        print(f'New customer {b} is added')
        break
    return c

def text(myresult):
    if myresult[5]==0 or myresult[5] ==None:
        b=0
    else:
        b=str(myresult[5])
    text=(f"""
        Customer ID:{myresult[0]}
        Customer Name: {(myresult[1])}
        Mobile Number:{str(myresult[2])}
        Email address:{str(myresult[3])}
        address:{str(myresult[4])}
        BALANCE: {b}
        """)        

    return text

def balanceupdate(bal,num):
    sql = f'UPDATE Customers SET Balance = {bal} WHERE MobNo = {num}'
    mycursor.execute(sql)
    mydb.commit()



def Pay():
    while True:
        n=(input('Mobile Number:'))
        if n.isnumeric  :
            if numcheck(n):
                num=n                         
                bio=search(num)
                c=True
                if biocheck(bio):
                    print(text(bio))
                    if (bio[5])!=0 and bio[5]!=None:         
                        while True:
                            pay=(input('How much the customer is paying = '))
                            if pay.isnumeric() and len(pay)< 19:
                                pay=int(pay)
                                if (bio[5])>=pay:
                                    balanceupdate((bio[5]-pay),num)
                                    print(f'Paid {pay} succesfully')
                                    bio=search(num)
                                    print('Remaining balance',(bio[5]))
                                    break
                                else:
                                    print('Your amount is higher than your value. !! Try again !!')
                                    continue
                            else:
                                print('Enter a valid amount')
                        break
                    else:
                        print(f'{bio[1]} Have Zero Balance')
                        break
                else:
                    c=True
                    print('customer not found')
                    while True:   
                        m=(input("exit or try again (e or t)")).lower()
                        if m=='e' :
                            c=False
                            print('Thank You')
                            break
                        elif m=='t' :
                            c=True
                            break
                        else:
                            print('invalid entry try again')
                            continue
                    if c==False:
                        break
                    else:continue
                
            else:
                    print('invalid number !! Try again !!')
            
                    continue
        else:
            continue 


def Lend():
    while True:
        n=(input('Mobile Number:'))
        if n.isnumeric  :
            if numcheck(n):
                num=n                         
                bio=search(num)
                c=True
                if biocheck(bio):
                    print(text(bio))
                    if bio[5]==None:  
                        sql = f"UPDATE Customers SET Balance = {0} WHERE MobNo = {num}"
                        mycursor.execute(sql)
                        mydb.commit()
                        while True:
                            lendd=input('How Much you want to lend = ')
                            if lendd.isnumeric() and len(lendd)<19:
                                lendd=int(lendd)
                                if lendd>0:
                                    balanceupdate((search(num)[5]+lendd),num)
                                    print(f'lended {lendd} succesfully')
                                    bio=search(num)
                                    print(f'''New balance{(bio[5])}''')
                                    break
                                else:
                                    print("You can't Enter zero amount")
                                    continue
                            else:
                                print('Enter a valid amount')
                        break
                    else:
                        while True:
                            lendd=input('How Much you want to lend = ')
                            if lendd.isnumeric() and len(lendd)<19:
                                lendd=int(lendd)
                                if lendd>0:
                                    balanceupdate((bio[5]+lendd),num)
                                    print(f'lended {lendd} succesfully')
                                    bio=search(num)
                                    print('New balance',(bio[5]))
                                    break
                                else:
                                    print("You can't Enter zero amount")
                                    continue
                            else:
                                print('Enter a valid amount')
                        break
                else:
                    c=True
                    print('customer not found')
                    while True:   
                        m=(input("exit or try again or add new customer (e or t or add)")).lower()
                        if m=='e' :
                            c=False
                            print('Thank You')
                            break
                        elif m=='t' :
                            c=True
                            break
                        elif m=='add':
                            if addcust():
                                c=True
                                print("New customer Added Try entering the new number")
                                break
                            else:
                                c=False
                        else:
                            print('invalid entry try again')
                            continue
                    if c==False:
                        break
                    else:
                        continue
                
            else:
                    print('invalid number !! Try again !!')
                    continue
        else:
            print('invalid number !! Try again !!')
            continue 

def addcustomer():
    addcust()
def custdetails():
    mycursor.execute("SELECT * FROM customers")
    myresult = mycursor.fetchall()
    if not myresult:
        print('No customers are found')
    else:
        for i in myresult:
            if  (i[5]) == None:
                details=(f"""
                Customer ID:{i[0]}
                Customer Name: {(i[1])}
                Mobile Number:{str(i[2])}
                Email address:{str(i[3])}
                address:{str(i[4])}
                BALANCE:0
                """)
            else:
                details=(f"""
                Customer ID:{i[0]}
                Customer Name: {(i[1])}
                Mobile Number:{str(i[2])}
                Email address:{str(i[3])}
                address:{str(i[4])}
                BALANCE:{str(i[5])}
                """)
            print(details)


def delcust():
    N=True
    while N:
        n=(input('Mobile Number:'))
        if n.isnumeric:
            if numcheck(n):
                num=n                         
                bio=search(num)
                c=True
                if biocheck(bio):
                    sql = f"DELETE FROM CUSTOMERS WHERE MobNo = {num}"
                    y_n = input("Are you sure you want to delete the customer :").lower()
                    
                    while True:
                        if y_n=='y':
                            mycursor.execute(sql)
                            print('Customer Successfully Deleted')
                            N=False
                            break
                        elif y_n=='n':
                            N=False
                            break
                        else:
                            print('invalid input !!TRY AGAIN!!')
                            break
                        
                else:
                    print('Customer not found ')
                    print('1.try again')
                    print('2.go back')
                    c=True
                    while True:
                        a=input('=>')
                        if a.isnumeric():
                            a=int(a)
                            if a == 1:
                                c=True
                                break
                            elif a == 2:
                                c=False
                                break
                            else:
                                print('Invalid input !Try again!')
                                continue
                        else:
                            print('Invalid input !Try again!')
                            continue
                    if c:
                        continue
                    else:
                        break
            else:
                print('invalid number !! Try again !!')
                continue
        else:
            print('invalid number !! Try again !!')
            continue 

def Searchcust():
    while True:
        n=(input('Mobile Number:'))
        if n.isnumeric  :
            if numcheck(n):
                num=n                         
                bio=search(num)
                c=True
                if biocheck(bio):
                    if (bio[5])!=0 and bio[5]!=None:         
                        x= str(bio[5])                             
                    else:
                        x=0
                    text=(f"""
                    Customer ID:{bio[0]}
                    Customer Name: {(bio[1])}
                    Mobile Number:{str(bio[2])}
                    Email address:{str(bio[3])}
                    address:{str(bio[4])}
                    BALANCE:{x}
                    """) 
                    print(text)
                    
                    break
                else:
                    c=True
                    print('customer not found')
                    m=(input("exit or try again or add new customer (e or t or add)")).lower()
                    if m=='e' :
                        c=False
                        print('Thank You')
                        break
                    elif m=='t' :
                        c=True
                        break
                    elif m=='add':
                        if addcust():
                            c=True
                            print("New customer Added Try entering the new number")
                            break
                        else:
                            c=False
                    else:
                        print('invalid entry try again')
                        continue
                if c==False:
                    break
                else:
                    continue
            else:
                    print('invalid number !! Try again !!')
            
                    continue


def main():
    e=[1,2,3,4,5,6]
    instruct='''
    1.Lend
    2.Pay
    3.Search customer
    4.Customer list
    5.Add Customer
    6.Delete customer
    Enter "Exit" to Exit the Program
    '''
    while True :
        print(instruct)
        enter=(input('=>'))
        if enter.isnumeric():
            enter=int(enter)
            if enter in e:
                if enter==1:
                    Lend()
                elif enter==2:
                    Pay()
                elif enter==3:
                    Searchcust()
                elif enter==4:
                    custdetails()
                elif enter==5:
                    addcustomer()
                elif enter==6:
                    delcust()
                
            else:
                print('Invalid input !!Try again!!')
        elif enter.lower()=='exit':
            print('Program closed')
            print('Thank you')
            break
        else:
            print('Invalid input !!Try again!!')
main()
