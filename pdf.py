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
#from stock import total, total2

#This is your data collected from your Vizard experiment
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