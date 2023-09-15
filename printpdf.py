from reportlab.pdfgen import canvas
my_path='my_pdf.pdf' 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from temp_marksheet import my_temp # import the template
c = canvas.Canvas(my_path,pagesize=letter)
c=my_temp(c) # run the template
c.setFillColorRGB(1,0,0)
c.setFont("Helvetica", 70)
c.drawRightString(6.4*inch,7.5*inch,'MARKSHEET')
c.setFillColorRGB(0,0,0)
c.setFont("Helvetica", 24)
c.drawRightString(2.5*inch,6.8*inch,'ID:')
c.drawRightString(2.5*inch,6*inch,'Name:')
c.drawRightString(2.5*inch,5*inch,'Class:')
c.drawRightString(2.5*inch,4*inch,'Gender:')
c.drawRightString(2.5*inch,3*inch,'Mark:')
c.drawRightString(3*inch,2*inch,'Grade:')
c.drawRightString(6*inch,-0.4*inch,'Signature')
# Conect to SQLite and collect the student details.
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
db_file='G:\\My drive\\testing\\my_db.db'  
try:
    file1='sqlite:///'+ db_file 
    my_conn = create_engine(file1)
    # For MySQL use the below line and remove the above lines for SQLite file
    #my_conn = create_engine("mysql+mysqldb://root:pw@localhost/my_tutorial")    
    r_set=my_conn.execute("SELECT *  FROM student WHERE id =6")
    data=r_set.fetchone()
    
except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    print(error)
## end of SQLite connection. 
c.setFillColorRGB(0,0,1)
c.setFont("Helvetica", 20)
c.drawString(3*inch,6.8*inch,str(data[0]))
c.drawString(3*inch,6*inch,data[1])
c.drawString(3*inch,5*inch,data[2])
c.drawString(3*inch,4*inch,data[4])
c.drawString(3*inch,3*inch,str(data[3]))
if(data[3]>=80):
    c.drawString(4*inch,2*inch,'A')
elif(data[3]>=60):
    c.drawString(4*inch,2*inch,'B')
else:
    c.drawString(4*inch,2*inch,'C')
c.showPage()
c.save()
