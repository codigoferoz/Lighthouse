from tkinter import *

def WarningPopup():
	warning = Toplevel()

	warning.title("Message")
	warning.geometry("230x100")


	l1=Label(warning, image="::tk::icons::question")
	l1.grid(row=0, column=0)
	l2=Label(warning,text="Are you sure you want to Quit")
	l2.grid(row=0, column=1, columnspan=3)

	#b1=Button(warning,text="Yes",command=ws.destroy, width=10)
	#b1.grid(row=1, column=1)
	b2=Button(warning,text="Aceptar",command=warning.destroy, width=10)
	b2.grid(row=1, column=2)

