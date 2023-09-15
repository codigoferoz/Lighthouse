from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from unicodedata import name



def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
    

def Users():
    
    global name_user,password,category
    global diskette,delete,edit,vocabulary,checklist,clean
    global SEARCH
    
    SEARCH = StringVar()
    name_user = StringVar()
    password = StringVar()
    category = StringVar()
    
    diskette = PhotoImage(file = "diskette.png")
    vocabulary = PhotoImage(file = "vocabulary.png")
    loupe = PhotoImage(file = "loupe.png")
    delete = PhotoImage(file = "delete.png")
    edit = PhotoImage(file = "edit.png")
    done = PhotoImage(file="done.png")
    calendar = PhotoImage(file = "calendar.png")
    duedate = PhotoImage(file="due_date.png")
    hourglass = PhotoImage(file="hourglass.png")
    checklist = PhotoImage(file="checklist.png")
    clean = PhotoImage(file="clean.png")
    low = PhotoImage(file="low-energy.png")
    fingerprint = PhotoImage(file="fingerprint.png")    
    
    def Update():
        Database()    
        name_user1=name_user.get()
        password1=password.get()
        category1=category.get()        
        if name_user1=='' or password1=='' or category1=='':
            tkMessageBox.showinfo("Warning","Complete los compos vacíos", parent = Users)
        else:        
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']        
            conn.execute('UPDATE REGISTRATION_USER SET name=?,password=?,category=? WHERE RID = ?',(name_user1,password1,category1,selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message","Modificación exitosa", parent = Users)        
            Reset()
            DisplayData()
            conn.close()

    def Register():
        Database()
        name_user1=name_user.get()
        password1=password.get()
        category1=category.get()        
        if name_user1=='' or password1==''or category1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = Users)
        else:
            conn.execute('INSERT INTO REGISTRATION_USER (name,password,category) \
                VALUES (?,?,?)',(name_user1,password1,category1));
            conn.commit()
            tkMessageBox.showinfo("Message","Registrado con éxito", parent = Users)
            DisplayData()
            conn.close()
            
    def Reset():
        tree.delete(*tree.get_children())
        DisplayData()
        SEARCH.set("")
        name_user.set("")
        password.set("")
        category.set("")
            
    def Delete():
        Database()
        if not tree.selection():
            tkMessageBox.showwarning("Warning","Select data to delete", parent = Users)
        else:
            result = tkMessageBox.askquestion('Confirm', 'Realmente quieres borrar este Usuario?', icon="warning", parent = Users)
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                cursor=conn.execute("DELETE FROM REGISTRATION_USER WHERE RID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()

    def SearchRecord():
        Database()
        if SEARCH.get() != "":
            tree.delete(*tree.get_children())
            cursor=conn.execute("SELECT * FROM REGISTRATION_USER WHERE NAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

    def DisplayData():    
        Database()    
        tree.delete(*tree.get_children())    
        cursor=conn.execute("SELECT * FROM REGISTRATION_USER")    
        fetch = cursor.fetchall()    
        for data in fetch:
            tree.insert('', 'end', values=(data))        
            tree.bind("<Double-1>",OnDoubleClick)
        cursor.close()
        conn.close()    
            
    def OnDoubleClick(self):
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']    
        name_user.set(selecteditem[1])
        password.set(selecteditem[2])
        category.set(selecteditem[3])
        
        
    Users=Toplevel() # Child window 
    Users.geometry("1200x600")  # Size of the window 
    Users.title("Usuarios")
    Users.iconbitmap('user.ico')
    
    Users.columnconfigure(
        0, 
        weight=1
    )
    Users.columnconfigure(
        1, 
        weight=3
    )
    
    LFrom = Frame(
        Users
    )
    LFrom.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
    )
    
    LeftViewForm = Frame(
        Users
    )
    LeftViewForm.grid(
        row=1, 
        column=1, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
        
    )
      
    MidViewForm = ttk.LabelFrame(
        Users, 
        text="Tabla de Usuarios", 
        padding=(5, 5)
    )
    MidViewForm.grid(
        row=0, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew",
        columnspan=3
    )
       
    Label(
        LFrom, 
        text="Nombre ", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=0, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    Entry(
        LFrom, 
        bd=2,
        font=("Arial",10,"bold"),
        textvariable=name_user
    ).grid(
        row=0, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom, 
        text="Password ", 
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
        LFrom, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=password
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom, 
        text="Categoría ", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=2, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    category.set("Seleccinone categoría")
    content={"Administrador","Operador"}
    OptionMenu(
        LFrom,
        category,
        *content
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom, 
        text="  Eliminar", 
        image=delete, 
        compound="left",
        command=Delete, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=6, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom, 
        text="  Modificar", 
        image=edit, 
        compound="left", 
        command=Update, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=6, 
        column=1, 
        padx=5, 
        pady=5
    )
    
    
    Button(
        LFrom,
        text="Guardar", 
        image=diskette, 
        compound="left", 
        font=("Arial", 10, "bold"),
        command=Register,
        fg="black",
        width=110
    ).grid(
        row=6, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )    
        
    
    Label(
        LeftViewForm, 
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
        LeftViewForm, 
        text="Insertar parámetros", 
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
        LeftViewForm, 
        bd=2, 
        textvariable=SEARCH, 
        font=('verdana', 10), 
        width=10
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5)
    
    Label(
        LeftViewForm, 
        text="Buscar por Nombre:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=2, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LeftViewForm,
        image=vocabulary,
        command=SearchRecord,
        font=('verdana', 10, "bold")
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LeftViewForm, 
        image=checklist, 
        compound="left", 
        text="  Mostrar Todos", 
        command=DisplayData,
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
        LeftViewForm, 
        text="  Limpiar",
        image=clean, 
        compound="left", 
        command=Reset,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=6, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    scrollbary = ttk.Scrollbar(MidViewForm)
    scrollbary.pack(side=RIGHT, fill=Y)     
   
    tree = ttk.Treeview(
        MidViewForm,
        columns=("User_id", "Name", "Password", "Category"),
        selectmode="extended", 
        height=15, show=("headings"),                   
        yscrollcommand=scrollbary.set,        
    )
    tree.pack(expand=True, fill=X)
    scrollbary.config(command=tree.yview)
    
    
    #setting treeview columns
    tree.heading('User_id', text="Id Usuario", anchor=W)
    tree.heading('Name', text="Nombre", anchor=W)
    tree.heading('Password', text="Password", anchor=W)    
    tree.heading('Category', text="Categoría", anchor=W)
        
    
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)       
    tree.pack()
    DisplayData()