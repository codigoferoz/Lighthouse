from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3


def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()

def Historial():
    
    global SEARCH_COMPLIANCE
    global compliance_id, id_task, description_task, due_date, compliance_date, user, id_device, device, details
    global checklist,fingerprint
    
    SEARCH_COMPLIANCE = StringVar()
    compliance_id = StringVar()
    id_task = StringVar()
    description_task = StringVar()
    due_date = StringVar()
    compliance_date = StringVar()
    user = StringVar()
    id_device = StringVar()
    device = StringVar()
    details = StringVar()
    
    checklist = PhotoImage(file="checklist.png")
    fingerprint = PhotoImage(file="fingerprint.png")
    
    def DisplayFinalize():
        Database()
        tree_compliance.delete(*tree_compliance.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_EXPIRATION")
        fetch = cursor.fetchall()
        for data in fetch:
            tree_compliance.insert('', 'end', values=(data))
            tree_compliance.bind("<Double-1>",OnDoubleClickFinalize)
        cursor.close()
        conn.close()

    def SearchFinalizeRecords():
        Database()
        if SEARCH_COMPLIANCE.get() != "":
            tree_compliance.delete(*tree_compliance.get_children())
            cursor=conn.execute("SELECT * FROM REGISTRATION_EXPIRATION WHERE ID_TASK LIKE ?", ('%' + str(SEARCH_COMPLIANCE.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree_compliance.insert('', 'end', values=(data))
            cursor.close()
            conn.close()  
    
    def OnDoubleClickFinalize(self):
        curItem = tree_compliance.focus()
        contents = (tree_compliance.item(curItem))
        selecteditem = contents['values']
        compliance_id.set(selecteditem[0])
        id_task.set(selecteditem[1])
        description_task.set(selecteditem[2])
        due_date.set(selecteditem[3])
        compliance_date.set(selecteditem[4])
        user.set(selecteditem[5])
        id_device(selecteditem[6])
        device(selecteditem[7])
        details.set("Detalle: " + selecteditem[1])
        
            
    historial=Toplevel() # Child window 
    historial.geometry("1200x600")  # Size of the window 
    historial.title("Histórico")
    historial.iconbitmap('history.ico')
    
    historial.columnconfigure(
        0, 
        weight=1
    )
    historial.columnconfigure(
        1, 
        weight=3
    )
    
    TopViewForm = Frame(
        historial
    )
    TopViewForm.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
    )
    
    LFrom = Frame(
        historial
    )
    LFrom.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=10, 
        sticky="nsew"
    )    
    
    MidViewForm = ttk.LabelFrame(
        historial,  
        text="Tabla de historial de transacciones", 
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
        LFrom, 
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
        LFrom, 
        bd=2, 
        textvariable=SEARCH_COMPLIANCE, 
        font=('verdana', 10), 
        width=10
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5)
    
    Label(
        LFrom, 
        text="Buscar por Id de tarea:", 
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
        LFrom, 
        image=fingerprint,
        command=SearchFinalizeRecords,
        font=('verdana', 10, "bold")
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        LFrom,
        image=checklist, 
        compound="left", 
        text=" Mostrar Todos", 
        command=DisplayFinalize,
        font=('verdana', 10, "bold")
    ).grid(
        row=6, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    #setting scrollbar
    scrollbary = ttk.Scrollbar(MidViewForm)
    scrollbary.pack(side=RIGHT, fill=Y)
    
    tree_compliance = ttk.Treeview(
        MidViewForm,
        columns=("Compliance_id", "Id_task", "Description_task", "Due_date","Compliance_date","User","Id_evice","Device"),
        selectmode="extended", 
        height=15, 
        yscrollcommand=scrollbary.set, 
        show=("headings")
    )
    tree_compliance.pack(expand=True, fill=X)
    scrollbary.config(command=tree_compliance.yview)
    
    
    #setting treeview columns
    tree_compliance.heading('Compliance_id', text="Id", anchor=W)
    tree_compliance.heading('Id_task', text="Id Tarea", anchor=W)
    tree_compliance.heading('Description_task', text="Descripción", anchor=W)
    tree_compliance.heading('Due_date', text="Vencimiento", anchor=W)
    tree_compliance.heading('Compliance_date', text="Finalización", anchor=W)
    tree_compliance.heading('User', text="Usuario", anchor=W)
    tree_compliance.heading('Id_evice', text="Id Dispositivo", anchor=W)
    tree_compliance.heading('Device', text="Dispositivo", anchor=W)
    
    tree_compliance.column('#0', stretch=NO, minwidth=0, width=0)
    tree_compliance.column('#1', stretch=NO, minwidth=0, width=40)
    tree_compliance.column('#2', stretch=NO, minwidth=0, width=60)
    tree_compliance.column('#3', stretch=NO, minwidth=0, width=350)
    tree_compliance.column('#4', stretch=NO, minwidth=0, width=80)
    tree_compliance.column('#5', stretch=NO, minwidth=0, width=80)
    tree_compliance.column('#6', stretch=NO, minwidth=0, width=80)
    tree_compliance.column('#7', stretch=NO, minwidth=0, width=80)
    tree_compliance.pack()    
    DisplayFinalize()