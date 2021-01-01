import binascii
import random
import string
result = ''
listascii = string.ascii_letters + string.digits
for j in range(72):
    for i in range(32):
        result = result+ (random.choice(listascii))
    result = result + "\n"
print (result)
f = open("banro.txt", "w")
f.write(result)


from fpdf import FPDF

# save FPDF() class into
# a variable pdf
pdf = FPDF()

# Add a page
pdf.add_page()

# set style and size of font
# that you want in the pdf
# pdf.add_font('Times', '', 'DejaVuSansCondensed.ttf', uni=True)
pdf.set_font("Courier", size=24)

# open the text file in read mode
f = open("banro.txt", "r")

# insert the texts in pdf
for x in f:
    pdf.cell(200, 10, txt=x, ln=1, align='C')

# save the pdf with name .pdf
pdf.output("banro.pdf")