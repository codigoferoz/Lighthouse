from tkinter import *
import tkinter.ttk as ttk
import datetime  
from datetime import date
import sqlite3
from threading import Timer




def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()



def Notification():
    
    global notifylabel
    notifylabel = StringVar()
    
    my_w_child=Toplevel() # Child window 
    my_w_child.geometry("600x200")  # Size of the window 
    my_w_child.title("¡Notificación!")
    my_w_child.iconbitmap('calendar.ico')
    
    lbl_alt = Label(my_w_child, textvariable=notifylabel, text="Listado de Tareas Vencidas", font=("Arial", 10, "bold"),bg="red",fg="white")
    lbl_alt.pack()
    #setting scrollbar
    
    scrollbary = Scrollbar(my_w_child, orient=VERTICAL)
    tree_notify = ttk.Treeview(my_w_child,columns=("Task_id", "Description", "Due_date"),selectmode="extended",height=14, yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree_notify.yview)
    scrollbary.pack(side=RIGHT, fill=Y)    
    
    #setting treeview columns 
    tree_notify.heading('Task_id', text="Id Tarea", anchor=W)
    tree_notify.heading('Description', text="Descripción", anchor=W)
    tree_notify.heading('Due_date', text="Vencimiento", anchor=W)
    
    
    tree_notify.column('#0', stretch=NO, minwidth=0, width=0)
    tree_notify.column('#1', stretch=NO, minwidth=0, width=40)
    tree_notify.column('#2', stretch=NO, minwidth=0, width=350)
    
    tree_notify.pack() 
    
    
    Database()
    today_date = date.today()
    soon = today_date + datetime.timedelta(int(15))
    
    if today_date != "":
        tree_notify.delete(*tree_notify.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE BETWEEN '2000-01-21' AND ?", (str(today_date), ))
        fetch = cursor.fetchall()
        tree_notify.tag_configure('expired', background="red", foreground= "white")
        for data in fetch:
            tree_notify.insert('', 'end', values=(data), tags='expired')
            
    if today_date != "":
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE BETWEEN ? AND ?", (str(today_date), str(soon), ))
        fetch = cursor.fetchall()
        tree_notify.tag_configure('soon', background="#FFFF33")
        for data in fetch:
            tree_notify.insert('', 'end', values=(data), tags='soon')       
                
        cursor.close()
        conn.close()
        
        notifylabel.set("¡HAY TAREAS QUE REQUIEREN SU ATENCION!")
        #winsound.Beep(440, 1000)
    else: 
        notifylabel.set("No se hallaron coincidencias")
        for i in tree_notify.get_children():
            tree_notify.delete(i)
         
    t = Timer(10.0, Notification)
    t.start() # after 28800 seconds or 8 hours 
        
 
     