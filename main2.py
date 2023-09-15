#-----------------------------------------------------------------------------
# Copyright (c) 2022, Ricardo Adrián López.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later).
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later)
#-----------------------------------------------------------------------------
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from tkcalendar import DateEntry
import datetime  
from datetime import date, timedelta
import tkinter  as tk
import datetime
from plyer import notification
import datetime as dt
from display_calendar import MyDateEntry

from devices import Devices
from finalize import Historial
from plot import graph_data
from stock import Stock
from users import Users
from write_csv import SaveToCsv
from notification import Notification
from categories import Category


#------------------------DATABASE------------------------
def Database():
    global conn, cursor
    #creating periodicity database
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
    #creating tables
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, DEVICE TEXT, LOCATION TEXT, CATEGORY TEXT, BRAND TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_TASK (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, DESCRIPTION TEXT, DUE_DATE TEXT, WHO_DOES_IT TEXT, ID_DEVICE TEXT, PERIODICITY TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_EXPIRATION (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ID_TASK TEXT, DESCRIPTION_TASK TEXT, DUE_DATE TEXT, COMPLIANCE_DATE TEXT, USER TEXT, ID_DEVICE TEXT, REMARK TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_SPARE (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, DESCRIPTION_SPARE TEXT, CRITICAL_STOCK TEXT, CURRENT_STOCK TEXT, REMARK_SPARE TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_USER (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, PASSWORD TEXT, CATEGORY TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_TYPE (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, TYPE TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS PLOTS (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, CRITICAL_STOCK TEXT, CURRENT_STOCK TEXT, ID_SPARE TEXT, SPARE)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS SPARE_STOCK (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, ID_SPARE TEXT, SPARE_QTY TEXT, SUPPLIER TEXT, BILL TEXT, ID_TASK TEXT, DATE_IN TEXT, PRICE TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS REGISTRATION_CATEGORY (RID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, CATEGORY TEXT, DESCRIPTION TEXT)")
#----------------------GUI LAYOUT------------------------
        
def DisplayForm():    
    display_screen = tk.Tk()    
    display_screen.geometry("1200x900")
    display_screen.wm_attributes('-toolwindow', 'false')    
    display_screen.iconbitmap('calendar.ico')
    display_screen.update_idletasks()  # Make sure every screen redrawing is done

    width, height = display_screen.winfo_width(), display_screen.winfo_height()
    x = int((display_screen.winfo_screenwidth() / 2) - (width / 2))
    y = int((display_screen.winfo_screenheight() / 2) - (height / 2))

    
     # Set a minsize for the window, and place it in the middle
    display_screen.minsize(width, height)
    display_screen.geometry(f"+{x}+{y}")
    
    menubar = Menu(display_screen)
    display_screen.config(menu=menubar)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Stock", command=Stock) 
    filemenu.add_command(label="Niveles", command=graph_data)    
    filemenu.add_command(label="Iniciar Alertas", command=Notification)
    filemenu.add_command(label="Dispositivos", command=Devices)
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=display_screen.quit)

    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Usuarios", command=Users)
    editmenu.add_command(label="Categorías", command=Category)
    editmenu.add_command(label="Historial", command=Historial)
   
   
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Ayuda")
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...")

    menubar.add_cascade(label="UTILIDADES", menu=filemenu)
    menubar.add_cascade(label="ADMINISTRACIÓN", menu=editmenu)
    menubar.add_cascade(label="AYUDA", menu=helpmenu)
               
    display_screen.title("LIGHTHOUSE - SISTEMA DE GESTION DE MANTENIMIENTO PROGRAMADO v02.00.00")
    display_screen.state("zoomed")
        
    global tree_task
    
    global SEARCH_TASK
    global description,due_date,who_does_it,id_device,periodicity
    global varckbtn,flash,details,remark,newlabel,id_task,next_due_date,user,compliance_date,id_device_compliance, description_device,due_date_history,cal,sel
    global clean,checklist,hourglass,duedate,calendar,vocabulary,done,edit,delete,loupe,diskette
    global limitsize
    
    
    SEARCH_TASK = StringVar()
    periodicity = StringVar()
    description = StringVar()
    due_date = StringVar()
    who_does_it = StringVar()
    id_device = StringVar()
    id_task = StringVar()
    next_due_date = StringVar()
    user = StringVar()
    compliance_date = DateEntry()
    id_device_compliance = StringVar()
    due_date_history = StringVar()
    description_device =StringVar()
    cal=StringVar()
    sel=StringVar()
    newlabel=StringVar()
    notifylabel=StringVar()
    remark=StringVar()
    details=StringVar()
    flash=StringVar()
    varckbtn=StringVar()
    limitsize=StringVar()
    
           

#-------------------GLOBAL STYLES-----------------------
    style = ttk.Style()
    style.theme_use('default')     
    style.configure(".", font=('Helvetica', 12, "bold"), foreground="black" , background="white")
    style.configure("Treeview.Heading", foreground="black", font=('Helvetica', 10, "bold"))
    #style.configure("TLabel", font=(''), foreground="black")#, background="red"


    diskette = PhotoImage(file = "diskette.png")    
    loupe = PhotoImage(file = "loupe.png")
    delete = PhotoImage(file = "delete.png")
    edit = PhotoImage(file = "edit.png")
    done = PhotoImage(file="done.png")
    vocabulary = PhotoImage(file = "vocabulary.png")
    calendar = PhotoImage(file = "calendar.png")
    duedate = PhotoImage(file="due_date.png")
    hourglass = PhotoImage(file="hourglass.png")
    checklist = PhotoImage(file="checklist.png")
    clean = PhotoImage(file="clean.png")
    
#-------------------------TASK FRAMES--------------------  
    #Settings frames   
    
    display_screen.columnconfigure(
        0, 
        weight=1
    )
    display_screen.columnconfigure(
        1, 
        weight=3
    )
    
    LFrom2 = Frame(
        display_screen
    )#, style="TLabel"
    LFrom2.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )
    
    Left3ViewForm2 = Frame(
        display_screen
    )
    Left3ViewForm2.grid(
        row=1, 
        column=1, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )
    
    MidViewForm2 = ttk.LabelFrame(
        display_screen, 
        text="Tabla de tareas", 
        padding=(5, 5)
    )
    MidViewForm2.grid(
        row=0, 
        column=0, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew", 
        columnspan=4
    )
    Left4ViewForm2 = Frame(
        display_screen
    )
    Left4ViewForm2.grid(
        row=1, 
        column=2, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )       
            
    lbl_alt2 = Label(
        MidViewForm2, 
        textvariable=newlabel, 
        text="Listado de Tareas", 
        font=("Arial", 10, "bold"),
        bg="#1A5276",
        fg="white"
    )
    lbl_alt2.pack(
        side=TOP, 
        pady=(0, 0),
        fill=X, 
        expand=True)    
    
    Label(
        LFrom2, 
        text="ALTA DE TAREAS", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=0, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
        )
    
    Label(
        LFrom2, 
        text="Descripción", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=1, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        LFrom2, 
        bd=2, 
        font=("Arial",10,"bold"),
        textvariable=description
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5)
    
    Label(
        LFrom2, 
        text="Vencimiento", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=3, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    cal2 = DateEntry(
        LFrom2, 
        bd=2, 
        textvariable=due_date, 
        width=18,
        background= "#1A5276", 
        foreground= "white", 
        date_pattern="yyyy-mm-dd"
    )
    cal2.delete(0,'end')
    cal2.grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom2, 
        text="Tipo Gestión", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=4, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    who_does_it.set("Seleccione tipo")
    content={"PROPIO","TERCEROS"}
    OptionMenu(
        LFrom2,
        who_does_it,
        *content
    ).grid(
        row=4, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5)
    
    
    Label(
        LFrom2, 
        text="ID Dispositivo", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=6, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        LFrom2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=id_device
    ).grid(
        row=6, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom2, 
        image=loupe, 
        command=DeviceList, 
        height= 30,
        width=30
    ).grid(
        row=6, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom2, 
        text="Frecuencia (días)", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=8, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Spinbox(
        LFrom2, 
        font=("Arial", 10, "bold"),
        textvariable=periodicity, 
        increment=1, 
        from_=0, 
        to=365
    ).grid(
        row=8, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left4ViewForm2, 
        text="BUSQUEDAS", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=0, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left4ViewForm2, 
        text="Insertar parámetros:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=1, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    search2 = MyDateEntry(
        Left4ViewForm2, 
        bd=2, 
        textvariable=SEARCH_TASK, 
        background= "#1A5276", 
        foreground= "white", 
        width=18, 
        date_pattern="yyyy-mm-dd"
    )
    search2.grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    search2.delete(0,'end')
    
    Label(
        Left4ViewForm2, 
        text="Buscar por Descripción:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=2, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    btn_search2 = Button(
        Left4ViewForm2, 
        image=vocabulary, 
        command=SearchRecordTask, 
        font=('verdana', 10, "bold")
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left4ViewForm2, 
        text="Buscar por Fecha:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=3, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Left4ViewForm2, 
        image=calendar, 
        command=SearchDueDateTask
    ).grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left4ViewForm2, 
        text="Buscar por vencidas:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=4, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Left4ViewForm2, 
        image=duedate, 
        command=ReportExpiredTask
    ).grid(
        row=4, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left4ViewForm2, 
        text="Buscar próximas a vencer:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=5, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Left4ViewForm2, 
        image=hourglass, 
        command=ExpireSoonTask
    ).grid(
        row=5, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    Button(
        Left4ViewForm2, 
        image=checklist, 
        compound="left", 
        text="  Mostrar Todos", 
        command=DisplayDataTask,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=6, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Left4ViewForm2, 
        text="  Limpiar",
        image=clean, 
        compound="left", 
        command=ResetTask,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=6, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom2, 
        text="  Eliminar", 
        image=delete, 
        compound="left",
        command=DeleteTask, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=9, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom2, 
        text="  Modificar", 
        image=edit, 
        compound="left", 
        command=UpdateTask, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=9, 
        column=1, 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom2, 
        text="  Guardar", 
        image=diskette, 
        compound="left", 
        font=("Arial", 10, "bold"), 
        command=register_task,
        fg="black", 
        width=110
    ).grid(
        row=9, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left3ViewForm2, 
        text="FINALIZACION DE TAREAS", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=0, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left3ViewForm2, 
        text="Id Tarea", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=1, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        Left3ViewForm2, 
        bd=2, 
        state='disabled',
        font=("Arial", 10, "bold"),
        textvariable=id_task
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left3ViewForm2, 
        text="Usuario", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=2, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        Left3ViewForm2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=user
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Left3ViewForm2, 
        image=loupe, 
        command=UsersList, 
        height= 30,
        width=30
    ).grid(
        row=2, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Left3ViewForm2, 
        text="Fecha Finalización", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=3, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    cal = DateEntry(
        Left3ViewForm2, 
        bd=2, 
        textvariable=next_due_date, 
        width= 18, 
        background= "#1A5276", 
        foreground= "white", 
        date_pattern="yyyy-mm-dd"
    )
    cal.delete(0,'end')
    cal.grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    def limitSize(*args):
        value = limitsize.get()
        if len(value) > 10: limitsize.set(value[:10])    
    
    limitsize.trace('w', limitSize)
    
    Label(Left3ViewForm2, text="Próximo mantenimiento", font=("Arial", 10, "bold"),fg="black").grid(row=4, column=0, sticky="W", padx=5, pady=10)
    next_due_date = Entry(
        Left3ViewForm2,
        textvariable=limitsize,          
        bg="white",
        relief="solid", 
        fg="red",
        font="Arial 10 bold", 
        width=20,        
    )
    next_due_date.grid(row=4, column=1, sticky="W", padx=5, pady=5)
    
    Label(
        Left3ViewForm2, 
        text="Observaciones", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=5, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=10
    )
    
    Entry(
        Left3ViewForm2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=remark
    ).grid(
        row=5, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
     
    Button(
        Left3ViewForm2, 
        text="Finalizar", 
        image=done, 
        compound="left", 
        font=("Arial", 10, "bold"), 
        command=EndingTask, 
        fg="black"
    ).grid(
        row=6, 
        column=2, 
        sticky="E", 
        padx=5, 
        pady=5
    )
    
    # Scrollbar
    
    scrollbary = ttk.Scrollbar(MidViewForm2)
    scrollbary.pack(side=RIGHT, fill=Y)    

    # Treeview
    tree_task = ttk.Treeview(
        MidViewForm2,
        columns=("Task_id", "Description", "Due_date", "Type","Device_id","Periodicity"),
            height=10,
            selectmode="extended",
            show=("headings"),                   
        yscrollcommand=scrollbary.set,        
    )
    tree_task.pack(expand=True, fill=X)
    scrollbary.config(command=tree_task.yview)    
    
    #setting treeview columns 
    tree_task.heading('Task_id', text="Id Tarea", anchor=W)
    tree_task.heading('Description', text="Descripción", anchor=W)
    tree_task.heading('Due_date', text="Vencimiento", anchor=W)
    tree_task.heading('Type', text="Gestión", anchor=W)
    tree_task.heading('Device_id', text="Id Dispositivo", anchor=W)
    tree_task.heading('Periodicity', text="Frecuencia", anchor=W)    
    
    tree_task.column('#0', stretch=NO, minwidth=0, width=0)
    tree_task.column('#1', stretch=NO, minwidth=0, width=40)
    tree_task.column('#2', stretch=NO, minwidth=0, width=850)
    tree_task.column('#3', stretch=NO, minwidth=0, width=130)
    tree_task.column('#4', stretch=NO, minwidth=0, width=80)    
    tree_task.column('#5', stretch=NO, minwidth=0, width=40)
    tree_task.pack() 
    
    Label(
        MidViewForm2, 
        bd=2, 
        justify=LEFT, 
        wraplength=800, 
        background="#AED6F1", 
        font=("Arial", 10, "bold"),
        textvariable=details
    ).pack(
        side=BOTTOM, 
        pady=(0, 0), 
        expand=True, 
        fill=X
    )
                    
    DisplayDataTask()   

#-----------------------TASK FUNCTIONS-----------------------

def DisplayDataTask():    
    Database()
    tree_task.delete(*tree_task.get_children())    
    cursor=conn.execute("SELECT * FROM REGISTRATION_TASK")
    fetch = cursor.fetchall()      
    for data in fetch: 
            tree_task.insert('', 'end', values=(data)) 
            tree_task.bind("<Double-1>",OnDoubleClickTask)
    cursor.close()
    conn.close()
    newlabel.set("Listado general de Tareas")
      
   
def OnDoubleClickTask(self):
    curItem = tree_task.focus()
    contents = (tree_task.item(curItem))
    selecteditem = contents['values']
    id_task.set(selecteditem[0])
    description.set(selecteditem[1])
    due_date.set(selecteditem[2])
    who_does_it.set(selecteditem[3])
    id_device.set(selecteditem[4])
    periodicity.set(selecteditem[5])
    details.set("Detalle: " + selecteditem[1])    
    NextDueDate()

def UpdateTask():
    Database()
    description1=description.get()
    due_date1=due_date.get()
    who_does_it1=who_does_it.get()
    id_device1=id_device.get()
    periodicity1=periodicity.get()
    if description1=='' or due_date1==''or who_does_it1=='' or id_device1=='' or periodicity1=='':
        tkMessageBox.showinfo("Warning","Complete los campos vacíos")
    else:
        curItem = tree_task.focus()
        contents = (tree_task.item(curItem))
        selecteditem = contents['values']
        conn.execute('UPDATE REGISTRATION_TASK SET DESCRIPTION=?,DUE_DATE=?,WHO_DOES_IT=?,ID_DEVICE=?,PERIODICITY=? WHERE RID = ?',(description1,due_date1,who_does_it1,id_device1,periodicity1, selecteditem[0]))
        conn.commit()
        tkMessageBox.showinfo("Message","Modificación exitosa")
        ResetTask()
        DisplayDataTask()
        conn.close()
        
def EndingTask():
    Database()
    id_task1=id_task.get()
    description1=description.get()
    next_due_date1=next_due_date.get()
    due_date1=due_date.get()
    compliance_date1=compliance_date.get()
    user1=user.get()    
    id_device1=id_device.get()    
    remark1=remark.get()   
    
    if id_task1=='' or description1=='' or next_due_date1=='' or due_date1=='' or compliance_date1=='' or user1=='' or id_device1==''or remark1=='' :
        tkMessageBox.showinfo("Warning","Complete los campos vacíos")
    else:
        curItem = tree_task.focus()
        contents = (tree_task.item(curItem))
        selecteditem = contents['values']
        conn.execute('UPDATE REGISTRATION_TASK SET DUE_DATE=? WHERE RID = ?',(next_due_date1, selecteditem[0]))
        conn.commit()
        conn.execute('INSERT INTO REGISTRATION_EXPIRATION (ID_TASK, DESCRIPTION_TASK, DUE_DATE, COMPLIANCE_DATE, USER, ID_DEVICE, REMARK) \
              VALUES (?,?,?,?,?,?,?)',(id_task1,description1,due_date1,compliance_date1,user1,id_device1,remark1));
        conn.commit()
        conn.execute('DELETE FROM SPARE_STOCK WHERE ID_TASK =?',(id_task1))
        conn.commit()
        #print()
        tkMessageBox.showinfo("Message","La tarea se ha finalizado con éxito")
        ResetTask()
        DisplayDataTask()
        #DisplayFinalize()
        conn.close()

def NextDueDate(): 
    today_date = date.today()
    td = timedelta(days=int(periodicity.get()))
    sel=str(today_date + td)   
    next_due_date.insert(0, sel)
 
def register_task():
    Database()
    description1=description.get()
    due_date1=due_date.get()
    who_does_it1=who_does_it.get()
    id_device1=id_device.get()
    periodicity1=periodicity.get()
    
    if description1==''or due_date1==''or who_does_it1=='' or periodicity1=='' or id_device1=='':
        tkMessageBox.showinfo("Warning","Complete los campos vacíos")
    else:
        conn.execute('INSERT INTO REGISTRATION_TASK (DESCRIPTION,DUE_DATE,WHO_DOES_IT,ID_DEVICE,PERIODICITY) \
              VALUES (?,?,?,?,?)',(description1,due_date1,who_does_it1,id_device1,periodicity1));
        conn.commit()
        tkMessageBox.showinfo("Message","Guardado con éxito")
        DisplayDataTask()
        SaveToCsv()
        conn.close()

def DeleteTask():
    Database()
    if not tree_task.selection():
        tkMessageBox.showwarning("Warning","Seleccione un registro para eliminar")
    else:
        result = tkMessageBox.askquestion('Confirm', '¿Realmente desea eliminar este registro?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree_task.focus()
            contents = (tree_task.item(curItem))
            selecteditem = contents['values']
            tree_task.delete(curItem)
            cursor=conn.execute("DELETE FROM REGISTRATION_TASK WHERE RID = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def SearchRecordTask():
    Database()
    if SEARCH_TASK.get() != "":
        tree_task.delete(*tree_task.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DESCRIPTION LIKE ?", ('%' + str(SEARCH_TASK.get()) + '%',))
        fetch = cursor.fetchall()        
        for data in fetch:
            tree_task.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        newlabel.set("Tareas que coinciden con la descripción ingresada")
    else: 
        newlabel.set("No se hallaron coincidencias")
        for i in tree_task.get_children():
            tree_task.delete(i) 

def SearchDueDateTask():
    Database()
    if SEARCH_TASK.get() != "":
        tree_task.delete(*tree_task.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE LIKE ?", ('%' + str(SEARCH_TASK.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree_task.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
    else: 
        newlabel.set("No se hallaron coincidencias")
        for i in tree_task.get_children():
            tree_task.delete(i)

def ReportDueDateTask():    
    Database()
    if SEARCH_TASK.get() != "":    
        tree_task.delete(*tree_task.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE WHERE LIKE ?", ('%' + str(SEARCH_TASK.get()) + '%',))
        fetch = cursor.fetchall()
        tree_task.tag_configure('expired', background="orange")
        tree_task.tag_configure('notexpired', background="green")
        for data in fetch:
            tree_task.insert('', 'end', values=(data), tags='expired')        
            tree_task.bind("<Double-1>",OnDoubleClickTask)
        cursor.close()
        conn.close()
        newlabel.set("Tareas que coinciden con la fecha ingresada")
    else: 
        newlabel.set("No se hallaron coincidencias")
        for i in tree_task.get_children():
            tree_task.delete(i)
    
def ReportExpiredTask():
    Database()
    today_date = date.today()
    if SEARCH_TASK.get() != "":
        tkMessageBox.showwarning("Warning","El campo de búsqueda debe estar vacío")
    if SEARCH_TASK.get() == "":
        tree_task.delete(*tree_task.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE BETWEEN '2000-01-21' AND ?", (str(today_date), ))
        fetch = cursor.fetchall()
        tree_task.tag_configure('expired', background="red", foreground= "white")
        for data in fetch:
            tree_task.insert('', 'end', values=(data), tags='expired')
        cursor.close()
        conn.close()
        newlabel.set("Tareas que están vencidas")
    else: 
        newlabel.set("No se hallaron coincidencias")
        for i in tree_task.get_children():
            tree_task.delete(i)
        
def ExpireSoonTask():
    Database() 
    today_date = date.today()
    soon = today_date + datetime.timedelta(int(15))
    if SEARCH_TASK.get() != "":
        tkMessageBox.showwarning("Warning","El campo de búsqueda debe estar vacío")
    if SEARCH_TASK.get() == "":
        tree_task.delete(*tree_task.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK WHERE DUE_DATE BETWEEN ? AND ?", (str(today_date), str(soon), ))
        fetch = cursor.fetchall()
        tree_task.tag_configure('soon', background="#FFFF33")
        for data in fetch:
            tree_task.insert('', 'end', values=(data), tags='soon')
        cursor.close()
        conn.close()
        newlabel.set("Tareas que se vencerán en los próximos 15 días")
    else: 
        newlabel.set("No se hallaron coincidencias")
        for i in tree_task.get_children():
            tree_task.delete(i)   

def ResetTask():
    tree_task.delete(*tree_task.get_children())
    DisplayDataTask()
    SEARCH_TASK.set("")
    description.set("")
    due_date.set("")
    who_does_it.set("Seleccione tipo")    
    id_device.set("")
    periodicity.set("")
    id_task.set("")
    user.set("")
    remark.set("")
    next_due_date.delete(0,"end")
    newlabel.set("Listado general de Tareas")
    details.set("")    
#-----------------------DEVICE LIST FUNCTIONS-----------------------
def DeviceList():
    Dlist_child=Toplevel() # Child window 
    Dlist_child.geometry("600x200")  # Size of the window 
    Dlist_child.title("Seleccione dispositivo")
    Dlist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
    Dlist_child.iconbitmap('device.ico')
        
    #setting scrollbar
    
    scrollbary = Scrollbar(Dlist_child, orient=VERTICAL)
    tree_device = ttk.Treeview(Dlist_child,columns=("Device_id", "Description", "Location"),selectmode="extended",height=14, yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree_device.yview)
    scrollbary.pack(side=RIGHT, fill=Y)    
    
    #setting treeview columns 
    tree_device.heading('Device_id', text="Id Tarea", anchor=W)
    tree_device.heading('Description', text="Descripción", anchor=W)
    tree_device.heading('Location', text="Ubicación", anchor=W)
    
    
    tree_device.column('#0', stretch=NO, minwidth=0, width=0)
    tree_device.column('#1', stretch=NO, minwidth=0, width=40)
    tree_device.column('#2', stretch=NO, minwidth=0, width=350)
    
    tree_device.pack()     
    
    def OnDoubleClick(self):
        curItem = tree_device.focus()
        contents = (tree_device.item(curItem))
        selecteditem = contents['values']    
        id_device.set(selecteditem[0])
        Dlist_child.destroy()
    
    Database()
    tree_device.delete(*tree_device.get_children())
    cursor=conn.execute("SELECT * FROM REGISTRATION")
    fetch = cursor.fetchall()
    #tree_device.tag_configure('expired', background="red", foreground= "white")
    for data in fetch:
        tree_device.insert('', 'end', values=(data))#, tags='expired'
        tree_device.bind("<Double-1>",OnDoubleClick)                
    cursor.close()
    conn.close()
    
#-----------------------USERS LIST FUNCTIONS-----------------------
def UsersList():
    Ulist_child=Toplevel() # Child window 
    Ulist_child.geometry("300x200")  # Size of the window 
    Ulist_child.title("Seleccione usuario")
    Ulist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
    Ulist_child.iconbitmap('user.ico')
        
    #setting scrollbar
    
    scrollbary = Scrollbar(Ulist_child, orient=VERTICAL)
    tree_users = ttk.Treeview(Ulist_child,columns=("User_id", "Name"),selectmode="extended",height=14, yscrollcommand=scrollbary.set)
    scrollbary.config(command=tree_users.yview)
    scrollbary.pack(side=RIGHT, fill=Y)    
    
    #setting treeview columns 
    tree_users.heading('User_id', text="Id Usuario", anchor=W)
    tree_users.heading('Name', text="Nombre", anchor=W)
       
    tree_users.column('#0', stretch=NO, minwidth=0, width=0)
    tree_users.column('#1', stretch=NO, minwidth=0, width=80)
        
    tree_users.pack()     
    
    def OnDoubleClick(self):
        curItem = tree_users.focus()
        contents = (tree_users.item(curItem))
        selecteditem = contents['values']    
        user.set(selecteditem[0])
        Ulist_child.destroy()
    
    Database()
    tree_users.delete(*tree_users.get_children())
    cursor=conn.execute("SELECT * FROM REGISTRATION_USER")
    fetch = cursor.fetchall()
    #tree_device.tag_configure('expired', background="red", foreground= "white")
    for data in fetch:
        tree_users.insert('', 'end', values=(data))#, tags='expired'
        tree_users.bind("<Double-1>",OnDoubleClick)                
    cursor.close()
    conn.close()




DisplayForm()
if __name__=='__main__':
    #Running Application
    mainloop()

