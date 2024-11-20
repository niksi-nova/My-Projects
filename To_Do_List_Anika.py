import mysql.connector.
import tabulate
import random
import smtplib
from tkinter import *
from tkinter import messagebox

#Creating Mysql Tables
cnx=mysql.connector.connect(user='root',passwd='123',host='localhost')
cursor=cnx.cursor()
cursor.execute("drop database if exists proj1")
cnx.commit()
query="create database proj1"

cursor.execute(query)
cnx.commit()

cursor.execute("use proj1")
cursor.execute("create table login(email varchar(30) primary key, password varchar(20))")
cnx.commit()




#Main Code
root=Tk()
root.title("Login or Sign up")

def menu1():
    root3=Tk()
    root3.title("Choose action")
    
    def add_task():
        root4=Tk()
        root4.title("Add task")
        l=Label(root4,text="Enter task")
        l.pack()
        e7=Entry(root4,width=100)
        e7.pack()
        l1=Label(root4,text="Enter due date (YYYY-MM-DD)")
        l1.pack()
        e8=Entry(root4,width=100)
        e8.pack()
        
        def add():
            task=e7.get()
            due=e8.get()
            query="insert into {} values('{}','{}',default)".format(name,task,due)
            cursor.execute(query)
            cnx.commit()
            l2=Label(root4,text="Task added!")
            l2.pack()
            root4.destroy()
            
        bu=Button(root4,text="Enter",command=add)
        bu.pack()

        
        root4.mainloop()

    def view_pending():
        root5=Tk()
        root5.title("View pending tasks")
        l10=Label(root5,text="Pending tasks")
        l10.pack()
        cursor.execute("select task,due from {} where status=false order by due desc".format(name))
        d=cursor.fetchall()
        p=Label(root5,text="    Task                         Due on",font=('Broadway 20'))
        p.pack(pady=10)

        def chk():
            cursor.execute("update {} set status=true where task = '{}'".format(name,o))
            cnx.commit()
        for i in d:
            o,w=i
            q=str(o)+" "*(35-len(str(o)))+str(w)
            ch=Button(root5,text="Click to mark completed",command=chk)
            z=Label(root5,text=q, font=('Broadway 15'))
            z.pack(pady=10)
            ch.pack(pady=150)
            #mark as completed not working properly    
           
            
            


        root5.mainloop()

    def view_completed():
        root6=Tk()
        root6.title("View completed tasks")
        l10=Label(root6,text="Pending tasks")
        l10.pack()
        cursor.execute("select task from {} where status=true".format(name))
        d=cursor.fetchall()
        p=Label(root6,text="Task",font=('Broadway 20'))
        p.pack(pady=10)
        for i in d:
            q=i
            z=Label(root6,text=q, font=('Broadway 20'))
            z.pack(pady=10)

        root6.mainloop()

        
    bu1=Button(root3,text="Add new task",command=add_task)
    bu1.pack()
    bu2=Button(root3,text="View pending tasks",command=view_pending)
    bu2.pack()
    bu3=Button(root3,text="View completed tasks",command=view_completed)
    bu3.pack()
    root3.mainloop()
    

#when login button clicked
def login():
    #Entering data
    root1=Tk()
    root1.title("Login")
    e=Entry(root1,width=50)
    l=Label(root1,text="Email ID")
    l.pack()
    e1=Entry(root1,width=50,show="*")
    l1=Label(root1,text="Password")
    e.pack()
    l1.pack()
    e1.pack()

    def enter3():
        global email
        global name
        email=e.get()
        passwd=e1.get()
        name=""
        for i in email:
            if i!="@":
                name+=i
            else:
                break

        #checking data
        cursor.execute("select * from login")
        d=cursor.fetchall()
        a=1
        for i in d:
            if i[0]==email:
                a=0
                if i[1]==passwd:
                    l2=Label(root1,text="Welcome!")
                    l2.pack()
                    menu1()
                    break
                else:
                    a=1
                    break
        if a==1:
            l3=Label(root1,text="Sorry, Email or password invalid!")
            l3.pack()
        

    b3=Button(root1,text="Enter",command=enter3)
    b3.pack()
    
    
        
                
    root1.mainloop()
    

#when signup button clicked
def signup():
    root2=Tk()
    root2.title("New user sign up")
    e=Entry(root2,width=50)
    l=Label(root2,text="Email ID")
    l.pack()
    e1=Entry(root2,width=50,show="*")
    l1=Label(root2,text="Set Password")
    e.pack()
    l1.pack()
    e1.pack()
    

    def enter1():
        
        email=e.get()
        passwd=e1.get()
        name=""
        for i in email:
            if i!="@":
                name+=i
            else:
                break

        #generate otp
        otp1=random.randint(0,9)
        otp2=random.randint(0,9)
        otp3=random.randint(0,9)
        otp=str(otp1)+str(otp2)+str(otp3)
        print(otp)

        #email otp
        smtp_object=smtplib.SMTP('smtp-mail.outlook.com',587)
        smtp_object.ehlo()
        smtp_object.starttls()
        smtp_object.login("anika.u.bhat@outlook.com","silver20")
        message="Subject:"+"Your otp is " + otp 
        smtp_object.sendmail("anika.u.bhat@outlook.com",email,message)
        smtp_object.quit()

        #enter otp and check
        e3=Entry(root2,width=50)
        l5=Label(root2,text="Please enter OTP sent to your email ID")
        l5.pack()
        e3.pack()

        def enter2(): 
            otp_entered=e3.get()

            if otp_entered==otp:
                
                cursor.execute("insert into login values('{}','{}')".format(email,passwd))
                cnx.commit()
                cursor.execute("CREATE TABLE IF NOT EXISTS {} (Task varchar(150) primary key,Due date,status bool default false)".format(name))
                cnx.commit()
                l4=Label(root2,text="Success")
                l4.pack()
               
            else:
                l6=Label(root2,text="Unsuccessful!")
                l6.pack()
            
        b1=Button(root2,text="Enter",command=enter2)
        b1.pack()
        

    b=Button(root2,text="Enter",command=enter1)
    b.pack()

    
        

    
    
    root2.mainloop()
    
button_login=Button(root, text="Existing User",command=login)
button_login.grid(row=0,column=0)
button_signup=Button(root, text="Sign Up",command=signup)
button_signup.grid(row=0,column=1)        
root.mainloop()
