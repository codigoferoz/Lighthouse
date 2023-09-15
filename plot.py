from doctest import master
from tkinter import *
import tkinter.ttk as ttk
from tkcalendar import DateEntry
import tkinter.messagebox as tkMessageBox
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


def Database():
    global conn, cursor
    conn = sqlite3.connect("periodicity.db")
    cursor = conn.cursor()


def graph_data():        
        Glist_child=Toplevel() # Child window 
        Glist_child.geometry("800x600")  # Size of the window 
        Glist_child.title("Seleccione Tarea")
        Glist_child.wm_attributes('-topmost', 'true') # '-toolwindow'
        Glist_child.iconbitmap('checklist.ico')
        
        Database()
        cursor=conn.execute('SELECT DESCRIPTION_SPARE, CRITICAL_STOCK , REMARK_SPARE, CURRENT_STOCK FROM REGISTRATION_SPARE')
        spare=[]
        critical_stock=[]
        remark_spare=[]
        current_stock=[]
       


        for row in cursor.fetchall(): 
            spare.append(row[0])
            critical_stock.append(row[1])
            remark_spare.append(row[2])
            current_stock.append(row[3])
            

        matplotlib.use('TkAgg')
        
        ff = Figure(figsize=(6,6), dpi=80)
        xx = ff.add_subplot(111)
        width = 0.35
        ind = np.arange(len(spare))
        rects1 = xx.barh(ind - width/2, current_stock, width, label='Stock actual')
        rects2 = xx.barh(ind + width/2, critical_stock, width, label='Stock crítico')
        canvas = FigureCanvasTkAgg(ff, master=Glist_child)
        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT)
        

        #xx.set_ylabel('Cantidades')
        xx.set_title('NIVELES')
        xx.set_yticks(ind, spare)
        xx.legend()

        xx.bar_label(rects1, padding=3)
        xx.bar_label(rects2, padding=3)

        ff.tight_layout()