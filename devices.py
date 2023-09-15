from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3



def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
    

def Devices():
    
    global device,location,category,brand
    global diskette,delete,edit,vocabulary,checklist,clean,loupe
    global SEARCH
    
    SEARCH = StringVar()
    device = StringVar()
    location = StringVar()
    category = StringVar()
    brand = StringVar()
    
    diskette = PhotoImage(file = "diskette.png")
    vocabulary = PhotoImage(file = "vocabulary.png")
    loupe = PhotoImage(file = "loupe.png")
    delete = PhotoImage(file = "delete.png")
    edit = PhotoImage(file = "edit.png")    
    checklist = PhotoImage(file="checklist.png")
    clean = PhotoImage(file="clean.png")      
    
    def Update():
        Database()    
        device1=device.get()
        location1=location.get()
        category1=category.get()
        brand1=brand.get()
        if device1=='' or location1=='' or category1=='' or brand1=='':
            tkMessageBox.showinfo("Warning","Complete los compos vacíos", parent = Devices)
        else:        
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']        
            conn.execute('UPDATE REGISTRATION SET device=?,location=?,category=?,brand=? WHERE RID = ?',(device1,location1,category1,brand1, selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message","Modificado con éxito", parent = Devices)        
            Reset()
            DisplayData()
            conn.close()

    def register():
        Database()
        device1=device.get()
        location1=location.get()
        category1=category.get()
        brand1=brand.get()
        if device1=='' or location1==''or category1=='' or brand1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = Devices)
        else:
            conn.execute('INSERT INTO REGISTRATION (device,location,category,brand) \
                VALUES (?,?,?,?)',(device1,location1,category1,brand1));
            conn.commit()
            tkMessageBox.showinfo("Message","Registrado con éxito", parent = Devices)
            DisplayData()
            conn.close()
            
    def Reset():
        tree.delete(*tree.get_children())
        DisplayData()
        SEARCH.set("")
        device.set("")
        location.set("")
        category.set("")
        brand.set("")
            
    def Delete():
        Database()
        if not tree.selection():
            tkMessageBox.showwarning("Warning","Seleccione un dispositivo de la tabla", parent = Devices)
        else:
            result = tkMessageBox.askquestion('Confirm', 'Realmente quieres borrar este Dispositivo?', icon="warning", parent = Devices)
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                cursor=conn.execute("DELETE FROM REGISTRATION WHERE RID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()

    def SearchRecord():
        Database()
        if SEARCH.get() != "":
            tree.delete(*tree.get_children())
            cursor=conn.execute("SELECT * FROM REGISTRATION WHERE device LIKE ?", ('%' + str(SEARCH.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

    def DisplayData():    
        Database()    
        tree.delete(*tree.get_children())    
        cursor=conn.execute("SELECT * FROM REGISTRATION")    
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
        device.set(selecteditem[1])
        location.set(selecteditem[2])
        category.set(selecteditem[3])
        brand.set(selecteditem[4]) 

    #-----------------------CATEGORY LIST FUNCTIONS-----------------------
    def CategoryList():
        Clist_child=Toplevel() # Child window 
        Clist_child.geometry("600x200")  # Size of the window 
        Clist_child.title("Seleccione Categoría")
        Clist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
        Clist_child.iconbitmap('category.ico')
            
        #setting scrollbar
        
        scrollbary = Scrollbar(Clist_child, orient=VERTICAL)
        tree_device = ttk.Treeview(Clist_child,columns=("Task_id", "Description", "Location"),selectmode="extended",height=14, yscrollcommand=scrollbary.set)
        scrollbary.config(command=tree_device.yview)
        scrollbary.pack(side=RIGHT, fill=Y)    
        
        #setting treeview columns 
        tree_device.heading('Task_id', text="Id Tarea", anchor=W)
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
            category.set(selecteditem[1])
            Clist_child.destroy()
        
        Database()
        tree_device.delete(*tree_device.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_CATEGORY")
        fetch = cursor.fetchall()
        #tree_device.tag_configure('expired', background="red", foreground= "white")
        for data in fetch:
            tree_device.insert('', 'end', values=(data))#, tags='expired'
            tree_device.bind("<Double-1>",OnDoubleClick)                
        cursor.close()
        conn.close()
        
    Devices=Toplevel() # Child window 
    Devices.geometry("1200x600")  # Size of the window 
    Devices.title("Dispositivos")
    Devices.iconbitmap('device.ico')
    
    Devices.columnconfigure(
        0, 
        weight=1
    )
    Devices.columnconfigure(
        1, 
        weight=3
    )
    
    
    LFrom = Frame(
        Devices
    )
    LFrom.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
    )
    
    LeftViewForm = Frame(
        Devices
    )
    LeftViewForm.grid(
        row=1, 
        column=1, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"        
    )
   
    
    MidViewForm = ttk.LabelFrame(
        Devices, 
        text="Tabla de dispositivos", 
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
        text="ALTA DE DISPOSITIVOS ", 
        font=("Arial", 10, "bold"),fg="black"
    ).grid(
        row=0, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )    
    
    Label(
        LFrom, 
        text="Denominación ", 
        font=("Arial", 10, "bold"),fg="black"
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
        font=("Arial",10,"bold"),
        textvariable=device
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    Label(
        LFrom, 
        text="Ubicación ", 
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
        LFrom, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=location
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
       
    Label(
        LFrom, 
        text="Categoria ", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=3, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        LFrom, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=category
    ).grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom, 
        image=loupe, 
        command=CategoryList, 
        height= 30,
        width=30
    ).grid(
        row=3, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        LFrom, 
        text="Marca/Modelo", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=4, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        LFrom, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=brand
    ).grid(
        row=4, 
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
        row=5, 
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
        row=5, 
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
        command=register,
        fg="black",
        width=110
    ).grid(
        row=5, 
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
        fg="black",
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
        columns=("Device_id", "Description", "Location", "Category","Branch"),
        selectmode="extended", 
        height=15, 
        yscrollcommand=scrollbary.set
    )
    tree.pack(expand=True, fill=X)
    scrollbary.config(command=tree.yview)
    
    #setting treeview columns
    tree.heading('Device_id', text="Id Dispositivo", anchor=W)
    tree.heading('Description', text="Denominación", anchor=W)
    tree.heading('Location', text="Ubicación", anchor=W)
    tree.heading('Category', text="Categoría", anchor=W)
    tree.heading('Branch', text="Marca/Modelo", anchor=W)    
    
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=80)    
    tree.pack()
    DisplayData()