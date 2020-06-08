from tkinter import *
import socket
import requests
import bs4
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt

#code for city

try:
	socket.create_connection( ("www.google.com", 80))		
	res = requests.get("https://ipinfo.io")
	data = res.json()	
	city_name = data['city']
	
except OSError as e:
	print("issue ", e)

#code for temp

try:
	socket.create_connection( ("www.google.com", 80))	
	res = requests.get("https://ipinfo.io")
	data = res.json()
	city_name = data['city']

	city = city_name
	socket.create_connection( ("www.google.com", 80))
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address =  a1 + a2  + a3 		
	res = requests.get(api_address)

	data = res.json()
	main = data['main']

	temp = main['temp']
	
except OSError as e:
	print("issue ", e)
except KeyError as e1:
	print("check city name", e1)

#code for quote of the day

try:
	socket.create_connection(("www.google.com",80))
	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,"lxml")
	data= soup.find("img",{"class":"p-qotd"})
	qotd = data['alt']

except Exception as e:
	print("issue",e)
 

# Functions 


def f1():
	adst.deiconify()
	root.withdraw()

def f2():
	vist.deiconify()
	root.withdraw()
	stdata.delete(1.0,END)
	con = None
	try:
		con = connect("test1.db")	
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()	#returns list of tuples
		info = ""
		for d in data:
			info = info + "rno: " + str(d[0]) + " name: " + str(d[1]) + " marks: " + str(d[2]) + "\n"
		stdata.insert(INSERT,info)
	except Exception as e:
		showerror("failure","insert issue" + str(e))
	finally:
		if con is not None:
			con.close()	
 
 
def f3():
	upst.deiconify()
	root.withdraw()
	
def f4():
	dest.deiconify()
	root.withdraw()

def f5():
	con = None
	try:
		con = connect("test1.db")	
		cursor = con.cursor()
		sql = "SELECT * FROM student ORDER BY marks desc;"
		cursor.execute(sql)
		list = cursor.fetchall()
		list = list[:5]
		#print(list) 
		#print(list[:5])
		
		names = [lis[1] for lis in list]
		marks = [lis[2] for lis in list]
		#print(str(names))
		#print(marks)

		#plt.bar(names,marks,color='b')
		plt.bar(names, marks, color=('b','r','g','c','m'))
		plt.xlabel("names")					
		plt.ylabel("marks")
		plt.title("Batch Information")
		plt.show() 
		con.commit()
		
	except Exception as e:
		showerror("failure","insert issue" + str(e))
		con.rollback()
		
	finally:
		if con is not None:
			con.close()	


def fun():
	entrno.delete(0,END)
	entname.delete(0,END)
	entmarks.delete(0,END)

def f6():
	con = None
	try:
		con = connect("test1.db")	
		rno = int(entrno.get())
		name = entname.get()
		marks = int(entmarks.get())
		#print(name.isalpha())
		
		if rno < 0 :
			showerror("failure","rno should be greater than zero")
			fun()
			
			
		elif (len(name) < 2 or name.isdigit() ):
			showerror("failure","check name")
			fun()

		elif marks <= 0 or marks >= 100:
			showerror("failure","marks should be between 0 to 100")
			fun()

		else:
			args = (rno,name,marks)
			cursor = con.cursor()
			sql = "insert into student values('%d','%s','%d')"
			cursor.execute(sql % args)   
			con.commit()
			showinfo("success","record added")
			fun()
		
	except Exception as e:
		showerror("failure","insert issue" + str(e))
		con.rollback()
		fun()

	finally:
		if con is not None:
			con.close()	

def f7():
	root.deiconify()
	adst.withdraw()

def f8():
	root.deiconify()
	vist.withdraw()

def fun2():
	entrno1.delete(0,END)
	entname1.delete(0,END)
	entmarks1.delete(0,END)	

def f9():
	con = None
	try:
		con = connect("test1.db")	
		rno = int(entrno1.get())
		name = entname1.get()
		marks = int(entmarks1.get())
		cursor = con.cursor()
		cursor.execute("SELECT rowid FROM student WHERE rno = ?", (rno,))
		data=cursor.fetchall()
		if len(data)==0:
			showerror("issue",'There is no such rno')
			fun2()
		elif len(name) < 2 or name.isdigit() :
			showerror("failure","check name")
			fun2()
		elif marks <= 0 or marks >= 100:
			showerror("failure","marks should be between 0 to 100")
			fun2()
		else:
			sql_update_query = """Update student set name = ? , marks = ? where rno = ?"""
			data = (name,marks,rno)
			cursor.execute(sql_update_query, data) 
			con.commit()
			showinfo("success","Record updated")
			fun2()

	except Exception as e:
		showerror("failure","insert issue" + str(e))
		con.rollback()
		fun2()

	finally:
		if con is not None:
			con.close()	

def f10():
	root.deiconify()
	upst.withdraw()

def f11():
	con = None
	try:
		con = connect("test1.db")	
		rno = int(entrno2.get())
		cursor = con.cursor()
		cursor.execute("SELECT rowid FROM student WHERE rno = ?", (rno,))
		data=cursor.fetchall()
		if len(data)==0:
			showerror("issue",'There is no such rno')
			entrno2.delete(0,END)
		else:
			sql = 'DELETE FROM student WHERE rno=?'
			cursor.execute(sql, (rno,))
			con.commit()
			showinfo("success","Record deleted")
			entrno2.delete(0,END)
	
	except Exception as e:
		showerror("failure","insert issue" + str(e))
		con.rollback()
		entrno2.delete(0,END)
		
	finally:
		if con is not None:
			con.close()


def f12():
	root.deiconify()
	dest.withdraw()


# design of root window

root = Tk()
root.title("S. M. S")
root.geometry("815x500+400+100")
root.configure(background="pale green")
#root.resizable(False,False)

t1 = 'Location:' + city_name
t2 = 'Temp:' + str(temp) + u"\N{DEGREE SIGN}" + "C"
t3 = 'QOTD:' + qotd 
b1 = Button(root,text="ADD",font=("arial",18,"bold"),width=15,command = f1)
b2 = Button(root,text="VIEW",font=("arial",18,"bold"),width=15,command = f2)
b3 = Button(root,text="UPDATE",font=("arial",18,"bold"),width=15,command = f3)
b4 = Button(root,text="DELETE",font=("arial",18,"bold"),width=15,command = f4)
b5 = Button(root,text="CHARTS",font=("arial",18,"bold"),width=15,command = f5)
l1 = Label(root,text=t1,background = "pale green",font=("arial",18,"bold"))
l2 = Label(root,text=t2,background = "pale green",font=("arial",18,"bold"))
l3 = Label(root,text=t3,background = "pale green",font=("arial",18,"bold"))

b1.pack(pady=10)
b2.pack(pady=10)
b3.pack(pady=10)
b4.pack(pady=10)
b5.pack(pady=10)
l1.place(x=10 , y=400)
l2.place(x=643, y=400)
l3.place(x=10 , y=450)

# design of add student window

adst = Toplevel(root)
adst.title("Add Student")
adst.geometry("500x400+400+200")
adst.withdraw()
adst.configure(background = "sky blue")

lblrno = Label(adst,text="Enter rno",bg="sky blue",font=("arial",18,"bold"))
entrno = Entry(adst,bd=5,font=("arial",18,"bold"))
lblname = Label(adst,text="Enter name",bg="sky blue",font=("arial",18,"bold"))
entname = Entry(adst,bd=5,font=("arial",18,"bold"))
lblmarks = Label(adst,text="Enter marks",bg="sky blue",font=("arial",18,"bold"))
entmarks = Entry(adst,bd=5,font=("arial",18,"bold"))
btnsave = Button(adst,text="Save",font=("arial",18,"bold"),width=10,command = f6)	
btnback = Button(adst,text="Back",font=("arial",18,"bold"),width=10,command = f7)

lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnsave.pack(pady=5)	
btnback.pack(pady=5)


# design of view student window

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("500x400+400+200")
vist.withdraw()
vist.configure(background = "khaki")

stdata = ScrolledText(vist,width=30,height=20)
btnvback = Button(vist,text="Back",font=("arial",18,"bold"),width=10,command = f8)

stdata.pack(pady=10)	
btnvback.pack(pady=10)


# design of update student window

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x400+400+200")
upst.withdraw()
upst.configure(background = "light pink")

lblrno1 = Label(upst,text="Enter rno",background = "light pink",font=("arial",18,"bold"))
entrno1 = Entry(upst,bd=5,font=("arial",18,"bold"))
lblname1 = Label(upst,text="Enter name",background = "light pink",font=("arial",18,"bold"))
entname1 = Entry(upst,bd=5,font=("arial",18,"bold"))
lblmarks1 = Label(upst,text="Enter marks",background = "light pink",font=("arial",18,"bold"))
entmarks1 = Entry(upst,bd=5,font=("arial",18,"bold"))
btnsave1 = Button(upst,text="Save",font=("arial",18,"bold"),width=10,command = f9)	
btnback1 =  Button(upst,text="Back",font=("arial",18,"bold"),width=10,command = f10)

lblrno1.pack(pady=5)
entrno1.pack(pady=5)
lblname1.pack(pady=5)
entname1.pack(pady=5)
lblmarks1.pack(pady=5)
entmarks1.pack(pady=5)
btnsave1.pack(pady=5)	
btnback1.pack(pady=5)

# design of delete student window

dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry("500x400+400+200")
dest.withdraw()
dest.configure(background = "mediumpurple1")

lblrno2 = Label(dest,text="enter rno",background = "mediumpurple1",font=("arial",18,"bold"))
entrno2 = Entry(dest,bd=5,font=("arial",18,"bold"))
btnsave2 = Button(dest,text="Save",font=("arial",18,"bold"),width=10,command = f11)	
btnback2 =  Button(dest,text="Back",font=("arial",18,"bold"),width=10,command = f12)

lblrno2.pack(pady=5)
entrno2.pack(pady=5)
btnsave2.pack(pady=5)	
btnback2.pack(pady=5)

root.mainloop()











