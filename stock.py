from doctest import master
from tkinter import *
import tkinter.ttk as ttk
from turtle import right
from setuptools import Command
#from sqlalchemy import values
from tkcalendar import DateEntry
import tkinter.messagebox as tkMessageBox
import sqlite3
import datetime  
from datetime import date, timedelta

from display_calendar import MyDateEntry
from pdf import createReq
from plot import graph_data


def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()
  
#global res
#res = resultreq

def Stock():
    
    global id_spare,spare,spare_qty,critical_stock,date_in,supplier,bill,id_task_spare,diskette
    global addition,substraction,vocabulary,calendar,low,hourglass,checklist,clean,fingerprint,delete,edit
    global remark_spare,price,loupe,prov,graph,alert,invoice
    global sum_stock,free_stock,crit_stock,provisioned_stock,spare_name,resultreq,total_box
    global SEARCH_SPARE
    SEARCH_SPARE = StringVar()
    
    id_spare = StringVar()
    spare = StringVar()
    spare_qty = StringVar()
    critical_stock = StringVar()
    date_in = StringVar()
    supplier = StringVar()
    bill = StringVar()
    id_task_spare = StringVar()
    remark_spare = StringVar()
    price = StringVar()
    sum_stock = StringVar()
    provision_qty = StringVar()
    free_stock = StringVar()
    crit_stock = StringVar()
    provisioned_stock = StringVar()
    spare_name = StringVar()
    resultreq = StringVar()
    total_box = StringVar()
    
    
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
    prov = PhotoImage(file="import.png")
    substraction = PhotoImage(file="substraction.png")
    addition = PhotoImage(file="addition.png")
    graph = PhotoImage(file="graph.png")
    alert = PhotoImage(file="alert.png")
    invoice = PhotoImage(file="invoice.png")
       
    
    def DisplayStockMovement():
        Database()
        tree_stock.delete(*tree_stock.get_children())
        cursor=conn.execute("SELECT * FROM SPARE_STOCK")
        fetch = cursor.fetchall()
        for data in fetch:
            tree_stock.insert('', 'end', values=(data))
            tree_stock.bind("<Double-1>",OnDoubleClickMovement)
        cursor.close()
        conn.close()
        
    def DisplayStock():
        Database()
        tree_spare.delete(*tree_spare.get_children())                
        cursor=conn.execute("SELECT * FROM REGISTRATION_SPARE")
        fetch = cursor.fetchall()        
        for data in fetch:
            tree_spare.insert('', 'end', values=(data))
            tree_spare.bind("<Double-1>",OnDoubleClickStock) 
        cursor.close()
        conn.close()
    
        
    #-----------------------REQUISITION LIST FUNCTIONS-----------------------
    
    
    def multipleselect():
        
        def edit(event):

            if tree_requisition.identify_region(event.x, event.y) == 'cell':
                
                def ok(event):
                    """Change item value."""
                    tree_requisition.set(item, column, entry.get())
                    entry.destroy()

                column = tree_requisition.identify_column(event.x)  
                item = tree_requisition.identify_row(event.y) 
                x, y, width, height = tree_requisition.bbox(item, column) 
                value = tree_requisition.set(item, column)

            elif tree_requisition.identify_region(event.x, event.y) == 'heading':                 

                def ok(event):
                    """Change heading text."""
                    tree_requisition.heading(column, text=entry.get())
                    entry.destroy()

                column = tree_requisition.identify_column(event.x)
                x, y, width, _ = tree_requisition.bbox(tree_requisition.get_children('')[0], column)                
                y2 = y                
                while tree_requisition.identify_region(event.x, y2) != 'heading':  
                    y2 -= 1                
                y1 = y2
                while tree_requisition.identify_region(event.x, y1) == 'heading':
                    y1 -= 1
                height = y2 - y1
                y = y1
                value = tree_requisition.heading(column, 'text')

            elif tree_requisition.identify_region(event.x, event.y) == 'nothing': 
                column = tree_requisition.identify_column(event.x)                 
                x, y, width, height = tree_requisition.bbox(tree_requisition.get_children('')[-1], column)
                if event.y > y:

                    def ok(event):
                        """Change item value."""
                        tr=tree_requisition                        
                        item = tr.insert("", "end", values=("", ""))
                        tr.set(item, column, entry.get())
                        entry.destroy()

                    y += height
                    value = ""
                                        
                else:
                    return
            else:
                return
            # display the Entry   
            entry = ttk.Entry(tree_requisition) 
            entry.place(x=x, y=y, width=width, height=height,
                        anchor='nw') 
            entry.insert(0, value)  
            entry.bind('<FocusOut>', lambda e: entry.destroy())  
            entry.bind('<Return>', ok) 
            entry.focus_set()
                  
        
        Rlist_child=Toplevel()  
        Rlist_child.geometry("500x350")   
        Rlist_child.title("Requisición")
        Rlist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
        Rlist_child.iconbitmap('checklist.ico')
        
        sugested_supplier = StringVar()
        sugested_supplier.set("Escriba el Nombre del proveedor")
        topdf = StringVar()
        
        Rlist_child.columnconfigure(
            0, 
            weight=1
        )
        Rlist_child.columnconfigure(
            1, 
            weight=3
        )                       
        
    
            
        
    
        TView = ttk.LabelFrame(
            Rlist_child, 
            text="Tabla de tareas", 
            padding=(5, 5)
        )
        TView.grid(
            row=0, 
            column=0, 
            padx=(5, 5), 
            pady=(5, 5), 
            sticky="nsew", 
            columnspan=4
        )
        
        Form21 = ttk.Frame(
            Rlist_child
        )
        Form21.grid(
            row=1, 
            column=1, 
            padx=(5, 5), 
            pady=(5, 5), 
            sticky="nsew"
        )

        total_box = Entry(
            Form21, 
            bd=2, 
            font=("Arial", 10, "bold"),
            width=40,
            #textvariable=sugested_supplier
        ).grid(
            row=1, 
            column=0, 
            sticky="W", 
            padx=5, 
            pady=5
        )
        
          
        def printReq():
            global resultreq
            global total,total2
            reqItems = tree_requisition.selection()     
            
            for line in reqItems:
                total = tree_requisition.set(line,"#2")
            for line in reqItems:
                total2 = tree_requisition.set(line,"#1")
            
            fields = "{0:10}{1:40}\n".format(total, total2)
            t1.insert(END, fields)
            
            
         
        Button(
            Form21, 
            text="Finalizar", 
            image=done, 
            compound="left", 
            font=("Arial", 10, "bold"), 
            #command=calc_total,
            command=printReq,            
            fg="black"
        ).grid(
            row=1, 
            column=3, 
            sticky="E", 
            padx=5, 
            pady=5
        )       
        
        
        l1 = ttk.Label(Form21,  text='Your Data', width=10 )  # added one Label 
        l1.grid(row=2,column=0,padx=10,pady=10) 

        t1 = Text(Form21,  height=12, width=45,bg='white') # text box
        t1.grid(row=3,column=0,padx=10)
        
        fields = "{0:10}{1:40}\n".format("Cant", "Producto")
        t1.insert(END, fields) 

        b1=Button(Form21,text='Generar PDF',command=lambda:createReq())#gen_pdf
        b1.grid(row=4,column=0,padx=20,pady=10)

        ### get PDF file libraries  
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import Paragraph, Frame, Spacer, Image, Table, TableStyle, SimpleDocTemplate
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics.shapes import Drawing #string
        from reportlab.graphics.charts.textlabels import Label
        from reportlab.graphics.charts.legends import Legend
        
        time = datetime.datetime.today()
        date = time.strftime("%d-%m-%Y")
        # add Paragraph style ##
        
        subject1 = 'Adrian'
        subject2 = 'Miriam'
        results1 = [15,23,42,56,76]
        results2 = [34,67,94,31,56]


        def createReq():
        #take the data and make ready for paragraph
            def dataToParagraph(name, data):
            
                p = '<strong>Subject name: </strong>' + name + '<br/>' + '<strong>Data: </strong>  ('
                for i in range(len(data)):
                    p += str(data[i])
                    if i != len(data) - 1:
                        p += ', '
                    else:
                        p += ')'   
                return p

            #take the data and convert to list of strings ready for table
            def dataToTable(name, data):
            
                data = [str(x) for x in data]
                data.insert(0,name)
                return data


            #create the table for our document
            def myTable(tabledata):

                #first define column and row size
                colwidths = (70, 50, 50, 50, 50, 50)
                rowheights = (25, 20, 20)

                t = Table(tabledata, colwidths, rowheights)

                GRID_STYLE = TableStyle(
                [('GRID', (0,0), (-1,-1), 0.25, colors.black),
                ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
                )

                t.setStyle(GRID_STYLE)
                return t
    
             ########   Now lets put everything together.   ########

            # create a list and add the elements of our document (image, paragraphs, table, chart) to it
            story = []

            #define the style for our paragraph text
            styles = getSampleStyleSheet()
            styleN = styles['Normal']

            #First add the Vizard Logo
            im = Image("imrc_logo.jpg", width=1*inch, height=1*inch)
            im.hAlign = 'RIGHT'
            story.append(im)

            #add the title
            story.append(Paragraph("<strong>Results for Vizard Experiment</strong>",styleN))
            story.append(Spacer(1,.25*inch))

            #convert data to paragraph form and then add paragraphs
            story.append(Paragraph(dataToParagraph(subject1, results1),styleN))
            story.append(Spacer(1,.25*inch))
            story.append(Paragraph(dataToParagraph(subject2, results2),styleN))
            story.append(Spacer(1,.5*inch))

            #add our table - first prepare data and then pass this to myTable function
            tabledata = (
            ('', 'Trial 1', 'Trial 2', 'Trial 3','Trial 4','Trial 5'),
            dataToTable(subject1, results1),
            dataToTable(subject2, results2))

            story.append(myTable(tabledata))
            story.append(Spacer(1,.5*inch))

            #build our document with the list of flowables we put together
            doc = SimpleDocTemplate('mydoc.pdf',pagesize = letter, topMargin=0)
            doc.build(story) 
        
        
        

        #setting scrollbar
        
        scrollbary = Scrollbar(TView, orient=VERTICAL)
        tree_requisition = ttk.Treeview(TView,columns=("Id_spare","Description","Critical_stock"),selectmode="extended",height=10, yscrollcommand=scrollbary.set)
        scrollbary.config(command=tree_requisition.yview)
        scrollbary.pack(side=RIGHT, fill=Y)    
        
        #setting treeview columns 
        tree_requisition.heading('Id_spare', text="ID", anchor=W)        
        tree_requisition.heading('Description', text="Descripción", anchor=W)
        tree_requisition.heading('Critical_stock', text="Stock Crítico", anchor=W)
        tree_requisition["displaycolumns"]=("Description", "Critical_stock")
        tree_requisition.column('#0', stretch=NO, minwidth=0, width=0)
        tree_requisition.column('#1', stretch=NO, minwidth=0, width=300)
        tree_requisition.column('#2', stretch=NO, minwidth=0, width=120)
            
        tree_requisition.pack(expand=True, fill=X)  
        
        curItems = tree_spare.selection()        
        result=[(tree_spare.item(i)['values']) for i in curItems]        
        index = iid = 0
        for row in result:
            tree_requisition.insert("", index, iid, values=row)
            index = iid = index + 1
            tree_requisition.bind("<Double-1>",edit) 
            tree_requisition.bind("<ButtonRelease-1>",)
 
    def SearchRecordStock():
        Database()
        if SEARCH_SPARE.get() == "":
            tkMessageBox.showwarning("Warning","Inserte un parámetro de búsqueda", parent = stock)
        if SEARCH_SPARE.get() != "":
            tree_spare.delete(*tree_spare.get_children())
            cursor=conn.execute("SELECT * FROM REGISTRATION_SPARE WHERE DESCRIPTION_SPARE LIKE ?", ('%' + str(SEARCH_SPARE.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree_spare.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
        else:            
            tkMessageBox.showinfo("Warning","La consulta no obtuvo resultados", parent = stock) 
            
    def SearchBillStock():
        Database()
        if SEARCH_SPARE.get() == "":
            tkMessageBox.showwarning("Warning","Inserte un parámetro de búsqueda", parent = stock)
        if SEARCH_SPARE.get() != "":
            tree_stock.delete(*tree_spare.get_children())
            cursor=conn.execute("SELECT * FROM SPARE_STOCK WHERE BILL LIKE ?", ('%' + str(SEARCH_SPARE.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree_stock.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
        else:            
            tkMessageBox.showinfo("Warning","La consulta no obtuvo resultados", parent = stock)
    
    def SearchDateInStock():
        Database()
        if SEARCH_SPARE.get() != "":
            tree_stock.delete(*tree_stock.get_children())
            cursor=conn.execute("SELECT * FROM SPARE_STOCK WHERE DATE_IN LIKE ?", ('%' + str(SEARCH_SPARE.get()) + '%',))
            fetch = cursor.fetchall()
            for data in fetch:
                tree_stock.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
        else:             
            for i in tree_stock.get_children():
                tree_stock.delete(i) 
    
    def ReportCriticalStock():
        Database()        
        tree_spare.delete(*tree_spare.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_SPARE WHERE CRITICAL_STOCK >= CURRENT_STOCK")
        fetch = cursor.fetchall()
        tree_spare.tag_configure('expired', foreground= "red")
        for data in fetch:
            tree_spare.insert('', 'end', values=(data), tags='expired')
        cursor.close()
        conn.close()   
    
    def RegisterStock():
        Database()
        spare1=spare.get()
        critical_stock1=critical_stock.get()
        remark_spare1=remark_spare.get()
        current_stock1=0
        
        if spare1=='' or critical_stock1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = stock)
        else:
            conn.execute('INSERT INTO REGISTRATION_SPARE (description_spare,critical_stock,current_stock,remark_spare) \
                VALUES (?,?,?,?)',(spare1,critical_stock1,current_stock1,remark_spare1));
            conn.commit()            
            tkMessageBox.showinfo("Message","Registrado con éxito", parent = stock)
            DisplayStock()
            conn.close()
            
    def OnDoubleClickStock(self):
        curItem = tree_spare.focus()  
        contents = (tree_spare.item(curItem))
        selecteditem = contents['values']        
        spare.set(selecteditem[1])        
        critical_stock.set(selecteditem[2])
        remark_spare.set(selecteditem[3])
        id_spare.set(selecteditem[0])
        ShowStockMovement()
        TotalStock()
        #FreeStock()
        
    
    def UpdateSpare():
        Database()
        spare1=spare.get()
        critical_stock1=critical_stock.get()
        remark_spare1=remark_spare.get()
        
        
        if spare1=='' or critical_stock1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = stock)
        else:
            curItem = tree_spare.focus()
            contents = (tree_spare.item(curItem))
            selecteditem = contents['values']
            conn.execute('UPDATE REGISTRATION_SPARE SET DESCRIPTION_SPARE=?,CRITICAL_STOCK=?,REMARK_SPARE=? WHERE RID = ?',(spare1,critical_stock1,remark_spare1,selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message","Modificación exitosa", parent = stock)
            ResetSpare()
            DisplayStock()
            
    def DeleteSpare():
        Database()
        if not tree_spare.selection():
            tkMessageBox.showwarning("Warning","Seleccione un registro para eliminar", parent = stock)
        else:
            result = tkMessageBox.askquestion('Confirm', '¿Realmente desea eliminar este registro?',
                                            icon="warning", parent = stock)
            if result == 'yes':
                curItem = tree_spare.focus()
                contents = (tree_spare.item(curItem))
                selecteditem = contents['values']
                tree_spare.delete(curItem)
                cursor=conn.execute("DELETE FROM REGISTRATION_SPARE WHERE RID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()
                ResetSpare()
    
    def ResetSpare():
        tree_spare.delete(*tree_spare.get_children())
        DisplayStock()
        DisplayStockMovement()
        SEARCH_SPARE.set("")
        spare.set("")
        spare_qty.set("")
        critical_stock.set("")
        date_in.set("")
        supplier.set("")
        bill.set("")
        id_task_spare.set("")
        id_spare.set("")
        sum_stock.set("")
        price.set("")
        provision_qty.set("")
        crit_stock.set("")
        free_stock.set("")
    
    def ShowStockMovement():
        Database()
        id_spare1=id_spare.get()
        tree_stock.delete(*tree_stock.get_children())
        cursor=conn.execute("SELECT * FROM SPARE_STOCK WHERE ID_SPARE=?", ( id_spare1,))
        fetch = cursor.fetchall()
        for data in fetch:
            tree_stock.insert('', 'end', values=(data))
            tree_stock.bind("<Double-1>",OnDoubleClickMovement)
        cursor.close()
        conn.close()
        
    #-------------------- STOCK IN -------------------
    
    
    def RegisterStockMovement():
        Database()
        id_spare1=id_spare.get()
        spare_qty1=spare_qty.get()
        supplier1=supplier.get()
        bill1=bill.get()        
        date_in1=date_in.get()        
        price1=price.get()
        id_task1="Libre"
        
        if id_spare1=='' or spare_qty1=='' or supplier1=='' or bill1=='' or date_in1=='' or price1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = stock)
        else:
            conn.execute('INSERT INTO SPARE_STOCK (id_spare,spare_qty,id_task,supplier,bill,date_in,price)\
                VALUES (?,?,?,?,?,?,?)', (id_spare1,spare_qty1,id_task1,supplier1,bill1,date_in1,price1))
            conn.commit()
            conn.execute('UPDATE REGISTRATION_SPARE SET CURRENT_STOCK=CURRENT_STOCK+? WHERE RID =?',(spare_qty1,id_spare1));
            conn.commit()
            tkMessageBox.showinfo("Message","Guardado con éxito", parent = stock)   
            DisplayStock()
            DisplayStockMovement()
        
    
    
    def TotalStock():
        id_task_st="Libre"
        Database()
        curItem = tree_spare.focus()
        contents = (tree_spare.item(curItem))
        selecteditem = contents['values']
        cursor=conn.execute("SELECT SUM(SPARE_QTY) FROM SPARE_STOCK WHERE ID_SPARE=?",(selecteditem[0],))
        sum_stock.set(cursor.fetchone()[0])
        cursor=conn.execute("SELECT SUM(SPARE_QTY) FROM SPARE_STOCK WHERE ID_SPARE=? AND ID_TASK=?",(selecteditem[0],id_task_st))
        free_stock.set(cursor.fetchone()[0])        
        cursor=conn.execute("SELECT CRITICAL_STOCK FROM REGISTRATION_SPARE WHERE RID=?",(selecteditem[0],))
        crit_stock.set(cursor.fetchone()[0])
        cursor.close()
        conn.close()
        
        free_stock1=free_stock.get()
        print(free_stock1)
        print(type(crit_stock))
        crit_stock1=crit_stock.get()
        print(crit_stock1)
        print(type(crit_stock))
        
        if free_stock1 <= crit_stock1:
            tkMessageBox.showinfo("Warning","Realizar compra", parent = stock)
        #else:
            #tkMessageBox.showinfo("Warning","Stock verificado", parent = stock)
        
        
    def OnDoubleClickMovement(self):
        curItem = tree_stock.focus()  
        contents = (tree_stock.item(curItem))
        selecteditem = contents['values']        
        id_spare.set(selecteditem[1])        
        spare_qty.set(selecteditem[2])
        supplier.set(selecteditem[4])
        bill.set(selecteditem[5])
        date_in.set(selecteditem[6])
        price.set(selecteditem[7])
        provision_qty.set(1)
        id_task_spare.set(selecteditem[3])  
    
    def DeleteStock():
        Database()
        id_spare1=id_spare.get()
        spare_qty1=spare_qty.get()
        if not tree_stock.selection():
            tkMessageBox.showwarning("Warning","Seleccione un registro para eliminar", parent = stock)
        else:
            result = tkMessageBox.askquestion('Confirm', '¿Realmente desea eliminar este registro?',
                                            icon="warning", parent = stock)
            if result == 'yes':
                curItem = tree_stock.focus()
                contents = (tree_stock.item(curItem))
                selecteditem = contents['values']
                tree_stock.delete(curItem)
                cursor=conn.execute("DELETE FROM SPARE_STOCK WHERE RID = %d" % selecteditem[0])
                conn.commit()
                conn.execute('UPDATE REGISTRATION_SPARE SET CURRENT_STOCK=CURRENT_STOCK-? WHERE RID =?',(spare_qty1,id_spare1));
                conn.commit()
                cursor.close()
                conn.close()
                ResetSpare()
                
    def UpdateStock():
        Database()
        id_spare1=id_spare.get()        
        spare_qty1=spare_qty.get()        
        supplier1=supplier.get()
        bill1=bill.get()
        date_in1=date_in.get()
        price1=price.get()
        
        
        if id_spare1=='' or spare_qty1=='' or supplier1=='' or bill1=='' or date_in1=='' or price1=='':
            tkMessageBox.showinfo("Warning","Complete los campos vacíos", parent = stock)
        else:
            curItem = tree_stock.focus()
            contents = (tree_stock.item(curItem))
            selecteditem = contents['values']
            conn.execute('UPDATE SPARE_STOCK SET ID_SPARE=?,SPARE_QTY=?,SUPPLIER=?,BILL=?,DATE_IN=?,PRICE=? WHERE RID = ?',(id_spare1,spare_qty1,supplier1,bill1,date_in1,price1,selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message","Modificación exitosa", parent = stock)
            ResetSpare()
            DisplayStockMovement()  
    
    #-----------------------PROVISIONING FUNCTIONS-----------------------
    def ProvisionedStock():
        Database()
        id_task_spare1=id_task_spare.get()
        curItem = tree_stock.focus()
        contents = (tree_stock.item(curItem))
        selecteditem = contents['values']
        cursor=conn.execute("SELECT SUM(SPARE_QTY) FROM SPARE_STOCK WHERE ID_TASK=?",(id_task_spare1,))
        provisioned_stock.set(cursor.fetchone()[0])
        
        
    
    def Provision():
        ProvisionedStock()
        Database()
        id_task_spare1=id_task_spare.get()
        provision_qty1=provision_qty.get()
        provisioned_stock1=provisioned_stock.get()
        
        id_spare1=id_spare.get()
        spare_qty1=spare_qty.get()
        supplier1=supplier.get()
        bill1=bill.get()        
        date_in1=date_in.get()        
        price1=price.get()
        new_provisioned_stock1=provision_qty1+provisioned_stock1   
                
        if provision_qty1>spare_qty1 or id_task_spare1 in {'Libre'} or id_task_spare1=='' or id_spare1=='' or supplier1=='' or bill1=='' or date_in1=='' or price1=='':
            tkMessageBox.showinfo("Warning","Verifique haya suficiente stock en el ingreso seleccionado, que no falte completar algún campo y que haya seleccionado un Id de tarea", parent = stock)
        else:
            curItem = tree_stock.focus()
            contents = (tree_stock.item(curItem))
            selecteditem = contents['values']
            conn.execute('UPDATE SPARE_STOCK SET SPARE_QTY=SPARE_QTY-? WHERE RID = ?',(provision_qty1,selecteditem[0]))
            conn.commit()
            conn.execute('INSERT INTO SPARE_STOCK (id_spare,spare_qty,id_task,supplier,bill,date_in,price)\
                VALUES (?,?,?,?,?,?,?)', (id_spare1,provision_qty1,id_task_spare1,supplier1,bill1,date_in1,price1))
            conn.commit()
            conn.execute('UPDATE REGISTRATION_SPARE SET CURRENT_STOCK=CURRENT_STOCK-? WHERE RID =?',(provision_qty1,id_spare1))
            conn.commit()
            conn.execute("DELETE FROM SPARE_STOCK WHERE SPARE_QTY=0")
            conn.commit()            
            conn.execute('UPDATE REGISTRATION_TASK SET SPARES=? WHERE RID =?',(new_provisioned_stock1,id_task_spare1))
            conn.commit()            
            tkMessageBox.showinfo("Message","Provisionado con éxito", parent = stock)   
            DisplayStock()
            DisplayStockMovement()
            
            
    
    
    #-----------------------RELEASING FUNCTIONS-----------------------
    def Release():
        
        Database()
        id_task2="Libre"
        id_task1=id_task_spare.get()
        provision_qty1=provision_qty.get()
        id_spare1=id_spare.get()
        
        if not tree_stock.selection() or id_task1 in {'Libre'}:
            tkMessageBox.showwarning("Atención","Parece que no ha seleccionado un ingreso o el mismo ya está Libre", parent = stock)
            
        else:
            result = tkMessageBox.askquestion('Confirm', '¿Realmente desea liberar este repuesto?',
                                            icon="warning", parent = stock)
            if result == 'yes':
                curItem = tree_stock.focus()
                contents = (tree_stock.item(curItem))
                selecteditem = contents['values']
                conn.execute('UPDATE SPARE_STOCK SET ID_TASK=? WHERE RID = ?',(id_task2,selecteditem[0]))
                conn.commit()
                conn.execute('UPDATE REGISTRATION_SPARE SET CURRENT_STOCK=CURRENT_STOCK+? WHERE RID = ?',(provision_qty1,id_spare1))
                conn.commit()                
                tkMessageBox.showinfo("Message","El repuesto se ha liberado con éxito", parent = stock)   
                DisplayStock()
                DisplayStockMovement()  
                
    #-----------------------TASK LIST FUNCTIONS-----------------------
    def TaskList():
        Tlist_child=Toplevel() # Child window 
        Tlist_child.geometry("300x200")  # Size of the window 
        Tlist_child.title("Seleccione Tarea")
        Tlist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
        Tlist_child.iconbitmap('checklist.ico')
            
        #setting scrollbar
        
        scrollbary = Scrollbar(Tlist_child, orient=VERTICAL)
        tree_users = ttk.Treeview(Tlist_child,columns=("Task_id", "Description"),selectmode="extended",height=14, yscrollcommand=scrollbary.set)
        scrollbary.config(command=tree_users.yview)
        scrollbary.pack(side=RIGHT, fill=Y)    
        
        #setting treeview columns 
        tree_users.heading('Task_id', text="Id Tarea", anchor=W)
        tree_users.heading('Description', text="Descripción", anchor=W)
        
        tree_users.column('#0', stretch=NO, minwidth=0, width=0)
        tree_users.column('#1', stretch=NO, minwidth=0, width=80)
            
        tree_users.pack()     
        
        def OnDoubleClick(self):
            curItem = tree_users.focus()
            contents = (tree_users.item(curItem))
            selecteditem = contents['values']    
            id_task_spare.set(selecteditem[0])
            Tlist_child.destroy()
        
        Database()
        tree_users.delete(*tree_users.get_children())
        cursor=conn.execute("SELECT * FROM REGISTRATION_TASK")
        fetch = cursor.fetchall()
        #tree_device.tag_configure('expired', background="red", foreground= "white")
        for data in fetch:
            tree_users.insert('', 'end', values=(data))#, tags='expired'
            tree_users.bind("<Double-1>",OnDoubleClick)                
        cursor.close()
        conn.close()    
    
    stock=Toplevel() # Child window 
    stock.geometry("1200x600")  # Size of the window 
    stock.title("Stock")
    stock.iconbitmap('packages.ico')
    
    stock.columnconfigure(
        0, 
        weight=1
    )
    stock.columnconfigure(
        1, 
        weight=3
    )
    
    From1 = Frame(
        stock
    )
    From1.grid(
        row=1, 
        column=0, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )
    
    Form2 = Frame(
        stock
    )
    Form2.grid(
        row=1, 
        column=2, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )
    
    Form4 = Frame(
        stock
    )
    Form4.grid(
        row=1, 
        column=3, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew"
    )
    
    Form3 = ttk.LabelFrame(
        stock, 
        text="Tabla de Repuestos", 
        padding=(5, 5)
    )
    Form3.grid(
        row=0, 
        column=0, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew",
        columnspan=2
    )
    
    Form5 = ttk.LabelFrame(
        stock, 
        text="Tabla de Stock", 
        padding=(5, 5)
    )
    Form5.grid(
        row=0, 
        column=2, 
        padx=(5, 5), 
        pady=(5, 5), 
        sticky="nsew",
        columnspan=2
    )
    
    
    Label(
        From1, 
        text="ALTA DE REPUESTOS", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=2, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )  
    
    Label(
        From1, 
          text="Denominación", 
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
        From1, 
        bd=2,
        font=("Arial",10,"bold"),
        textvariable=spare
    ).grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5)
    
    Label(
        From1, 
        text="Stock Crítico", 
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
        From1, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=critical_stock
    ).grid(
        row=4, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        From1, 
        text="Observaciones", 
        font=("Arial", 10, "bold"),        
        fg="black"
    ).grid(
        row=5, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    Entry(
        From1, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=remark_spare
    ).grid(
        row=5, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
    Button(
        From1, 
        text="  Eliminar", 
        image=delete, 
        compound="left",
        command=DeleteSpare, 
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
        From1, 
        text="  Modificar", 
        image=edit, 
        compound="left", 
        command=UpdateSpare, 
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
        From1,
        text="Guardar", 
        image=diskette, 
        compound="left", 
        font=("Arial", 10, "bold"),
        command=RegisterStock,
        fg="black",
        width=110
    ).grid(
        row=6, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    ttk.Separator(
        From1,
        orient=HORIZONTAL   
    ).grid(
        row=7, 
        column=0, 
        columnspan=3, 
        sticky="nswe", 
        padx=2, 
        pady=15
    ) 
    
    Label(
        From1, 
        text="PROVISIONAMIENTO", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=8, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        From1, 
        text="Id Tarea", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=9, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    Entry(
        From1, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=id_task_spare
    ).grid(
        row=9, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        From1, 
        image=loupe, 
        command=TaskList, 
        height= 30,
        width=30
    ).grid(
        row=9, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        From1, 
        text="Cantidad", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=10, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    Entry(
        From1, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=provision_qty
    ).grid(
        row=10, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    
    Button(
        From1,
        text=" Provisionar", 
        image=addition,
        compound="left",
        font=("Arial", 10, "bold"),  
        command=Provision, 
        fg="black",
        width=110
    ).grid(
        row=11, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        From1,
        text=" Liberar", 
        image=substraction,
        compound="left",
        font=("Arial", 10, "bold"),  
        command=Release, 
        fg="black",
        width=110
    ).grid(
        row=11, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form2, 
        text="RECEPCION", 
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
        Form2, 
        text="Id Repuesto", 
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
        Form2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=id_spare
    ).grid(
        row=1, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form2, 
        text="Cantidad", 
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
        Form2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=spare_qty
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form2, 
        text="Proveedor", 
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
        Form2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=supplier
    ).grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form2, 
        text="Remito", 
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
        Form2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=bill
    ).grid(
        row=4, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )

    Label(
        Form2, 
        text="Fecha Ingreso", 
        font=("Arial", 10, "bold"),fg="black"
    ).grid(
        row=5, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    cal = DateEntry(
        Form2, 
        bd=2, 
        textvariable=date_in, 
        width= 20, 
        background= "#1A5276", 
        foreground= "white", 
        date_pattern="yyyy-mm-dd"
    )
    cal.delete(0,'end')
    cal.grid(
        row=5, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form2, 
        text="Precio", 
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
        Form2, 
        bd=2, 
        font=("Arial", 10, "bold"),
        textvariable=price
    ).grid(
        row=6, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Form2, 
        text="  Eliminar", 
        image=delete, 
        compound="left",
        command=DeleteStock, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=7, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Form2, 
        text="  Modificar", 
        image=edit, 
        compound="left", 
        command=UpdateStock, 
        fg="black", 
        font=('verdana', 10, "bold"), 
        width=110
    ).grid(
        row=7, 
        column=1, 
        padx=5, 
        pady=5
    )
    
    
    Button(
        Form2,
        text="Guardar", 
        image=diskette, 
        compound="left", 
        font=("Arial", 10, "bold"),
        command=RegisterStockMovement,
        fg="black",
        width=110
    ).grid(
        row=7, 
        column=2, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    ttk.Separator(
        Form2,
        orient=HORIZONTAL   
    ).grid(
        row=8, 
        column=0, 
        columnspan=3, 
        sticky="nswe", 
        padx=2, 
        pady=15
    ) 
    
    Label(
        Form2, 
        text="STOCK TOTAL:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=9, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        Form2, 
        state='disabled',
        bd=2,
        font=("Arial",10,"bold"),
        textvariable=sum_stock
    ).grid(
        row=9, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    
    Label(
        Form2, 
        text="STOCK LIBRE:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=10, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        Form2, 
        state='disabled',
        bd=2,
        font=("Arial",10,"bold"),
        textvariable=free_stock
    ).grid(
        row=10, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    
    Label(
        Form4, 
        text="CONSULTAS", 
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
        Form4, 
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
    
    search2 = MyDateEntry(
        Form4, 
        bd=2, 
        textvariable=SEARCH_SPARE, 
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
        Form4, 
        text="Buscar Repuesto por Descripción:", 
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
        Form4, 
        image=vocabulary, 
        command=SearchRecordStock, 
        font=('verdana', 10, "bold")
    ).grid(
        row=2, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form4, 
        text="Buscar por Fecha de Ingreso:", 
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
        Form4, 
        image=calendar, 
        command=SearchDateInStock
    ).grid(
        row=3, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form4, 
        text="Gráfico de niveles:", 
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
        Form4, 
        image=graph, 
        command=graph_data
    ).grid(
        row=4, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Label(
        Form4, 
        text="Buscar por N° de Remito:", 
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
        Form4, 
        image=invoice, 
        command=SearchBillStock
    ).grid(
        row=5, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
        
        
    Button(
        Form4, 
        text="  Limpiar",
        image=clean, 
        compound="left", 
        command=ResetSpare,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=6, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    ttk.Separator(
        Form4,
        orient=HORIZONTAL   
    ).grid(
        row=7, 
        column=0, 
        columnspan=3, 
        sticky="nswe", 
        padx=2, 
        pady=15
    ) 
    Label(
        Form4, 
        text="STOCK CRITICO:", 
        font=("Arial", 10, "bold"),
        fg="black"
    ).grid(
        row=8, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Entry(
        Form4, 
        state='disabled',
        bd=2,
        font=("Arial",10,"bold"),
        textvariable=crit_stock
    ).grid(
        row=8, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Form4, 
        text="  Mostrar niveles críticos",
        image=alert, 
        compound="left", 
        command=ReportCriticalStock,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=9, 
        column=0, 
        sticky="W", 
        padx=5, 
        pady=5
    )
    
    Button(
        Form4, 
        image=checklist, 
        compound="left", 
        text="  Mostrar Todos", 
        command=DisplayStock,
        fg="black", 
        font=('verdana', 10, "bold")
    ).grid(
        row=9, 
        column=1, 
        sticky="W", 
        padx=5, 
        pady=5
    )
               
    #------------------------ 1° TREEVIEW ----------------
    
    scrollbary = ttk.Scrollbar(Form3)
    scrollbary.pack(side=RIGHT, fill=Y)    

    tree_spare = ttk.Treeview(
        Form3,
        columns=("Id_spare", "Description","Critical_stock","Remark"),
            height=10,
            selectmode="extended",
            show=("headings"),                   
        yscrollcommand=scrollbary.set,        
    )
    tree_spare.pack(expand=True, fill=X)
    scrollbary.config(command=tree_spare.yview)
    
    #setting treeview columns
    tree_spare.heading('Id_spare', text="Id", anchor=W)    
    tree_spare.heading('Description', text="Descripción", anchor=W)  
    tree_spare.heading('Critical_stock', text="Stock Crítico", anchor=W)
    tree_spare.heading('Remark', text="Observaciones", anchor=W)
     
    tree_spare.column('#0', stretch=NO, minwidth=0, width=0)
    tree_spare.column('#1', stretch=NO, minwidth=0, width=40)
    tree_spare.column('#2', stretch=NO, minwidth=0, width=100)
    tree_spare.column('#3', stretch=NO, minwidth=0, width=60)
    tree_spare.pack()
    tree_spare.bind("<Return>", lambda e: multipleselect())    
    DisplayStock()
    
   #------------------------ 2° TREEVIEW ----------------
    
    scrollbary = ttk.Scrollbar(Form5)
    scrollbary.pack(side=RIGHT, fill=Y)    

    tree_stock = ttk.Treeview(
        Form5,
        columns=("Id_movement","Id_spare","Spare_qty","Id_task","Supplier","Bill","Date","Price"),
            height=10,
            selectmode="extended",
            show=("headings"),                   
        yscrollcommand=scrollbary.set,        
    )
    tree_stock.pack(expand=True, fill=X)
    scrollbary.config(command=tree_stock.yview)
    
    #setting treeview columns
    tree_stock.heading('Id_movement', text="Id", anchor=W)
    tree_stock.heading('Id_spare', text="Id Repuesto", anchor=W)    
    tree_stock.heading('Spare_qty', text="Cantidad", anchor=W)
    tree_stock.heading('Id_task', text="Id_Tarea", anchor=W)
    tree_stock.heading('Supplier', text="Proveedor", anchor=W)
    tree_stock.heading('Bill', text="Remito", anchor=W)    
    tree_stock.heading('Date', text="Fecha ingreso", anchor=W)
    tree_stock.heading('Price', text="Precio", anchor=W)
    
    tree_stock.column('#0', stretch=NO, minwidth=0, width=0)
    tree_stock.column('#1', stretch=NO, minwidth=0, width=30)
    tree_stock.column('#2', stretch=NO, minwidth=0, width=60)
    tree_stock.column('#3', stretch=NO, minwidth=0, width=60)
    tree_stock.column('#4', stretch=NO, minwidth=0, width=80)
    tree_stock.column('#5', stretch=NO, minwidth=0, width=130)
    tree_stock.column('#6', stretch=NO, minwidth=0, width=100)
    tree_stock.column('#7', stretch=NO, minwidth=0, width=100)
    tree_stock.pack()    
    DisplayStockMovement()

   

 