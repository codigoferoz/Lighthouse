from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
from unicodedata import name



def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
    

def Category():
    
    global description,category
    global diskette,delete,edit,vocabulary,checklist,clean
    global SEARCH
    
    SEARCH = StringVar()
    name_user = StringVar()
    password = StringVar()
    category = StringVar()
    description = StringVar()
    
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
        category1=category.get()    
        description1=description.get()      
                
        if category1=='' or description1=='':
            tkMessageBox.showinfo("Warning","Complete los compos vacíos", parent = Category)
        else:        
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']        
            conn.execute('UPDATE REGISTRATION_CATEGORY SET category=?,description=? WHERE RID = ?',(category1,description,selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message","Modificación exitosa", parent = Category)        
            Reset()
            DisplayData()
            conn.close()

    def Register():
        Database()
        category1=category.get()    
        description1=description.get()        
        if category1=='' or description1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = Category)
        else:
            conn.execute('INSERT INTO REGISTRATION_CATEGORY (category,description) \
                VALUES (?,?)',(category1, description1));
            conn.commit()
            tkMessageBox.showinfo("Message","Registrado con éxito", parent = Category)
            DisplayData()
            conn.close()
            
    def Reset():
        tree.delete(*tree.get_children())
        DisplayData()
        SEARCH.set("")        
        category.set("")
        description.set("")
            
    def Delete():
        Database()
        if not tree.selection():
            tkMessageBox.showwarning("Warning","Select data to delete", parent = Category)
        else:
            result = tkMessageBox.askquestion('Confirm', 'Realmente quieres borrar este Usuario?', icon="warning", parent = Category)
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                cursor=conn.execute("DELETE FROM REGISTRATION_CATEGORY WHERE RID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()

    def SearchRecord():
        Database()
        if SEARCH.get() != "":
            tree.delete(*tree.get_children())
            cursor=conn.execute("SELECT * FROM REGISTRATION_CATEGORY WHERE NAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

    def DisplayData():    
        Database()    
        tree.delete(*tree.get_children())    
        cursor=conn.execute("SELECT * FROM REGISTRATION_CATEGORY")    
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
        category.set(selecteditem[1])
        description.set(selecteditem[2])
        
        
    Category=Toplevel() # Child window 
    Category.geometry("1200x600")  # Size of the window 
    Category.title("Categorías")
    Category.iconbitmap('category.ico')
    
    Category.columnconfigure(
        0, 
        weight=1
    )
    Category.columnconfigure(
        1, 
        weight=3
    )
    
    LFrom = Frame(
        Category
    )
    LFrom.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
    )
    
    LeftViewForm = Frame(
        Category
    )
    LeftViewForm.grid(
        row=1, 
        column=1, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
        
    )
      
    MidViewForm = ttk.LabelFrame(
        Category, 
        text="Tabla de Categorías", 
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
        text="Categoría ", 
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
        textvariable=category
    ).grid(
        row=0, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom, 
        text="Descripción ", 
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
        textvariable=description
    ).grid(
        row=1, 
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
        text="Buscar por Categoría:", 
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
        columns=("User_id", "Category", "Description"),
        selectmode="extended", 
        height=15, show=("headings"),                   
        yscrollcommand=scrollbary.set,        
    )
    tree.pack(expand=True, fill=X)
    scrollbary.config(command=tree.yview)
    
    
    #setting treeview columns
    tree.heading('User_id', text="Id Categoría", anchor=W)
    tree.heading('Description', text="Descripción", anchor=W)    
    tree.heading('Category', text="Categoría", anchor=W)
        
    
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)      
    tree.pack()
    DisplayData()