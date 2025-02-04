from fpdf import FPDF

# PDF-Klasse erstellen
class PDF(FPDF):
    def __init__(self, header_line):
        self.header_line = header_line
        FPDF.__init__(self)

    def header(self):
        self.set_font('Courier', '', 12)  # Monospaced Font verwenden
        self.cell(0, 10, self.header_line, align='C', ln=True)
        self.ln(10)  # Zeilenumbruch

    def chapter_body(self, body):
        self.set_font('Courier', '', 8)  # Monospaced Font für Text
        self.multi_cell(0, 3, body)  # Multi_Cell sorgt für Textumbruch
        #self.ln()
# Funktion zum Umwandeln von TXT zu PDF
def txt_to_pdf(text, header, pdf_file):
    pdf = PDF(header)
    pdf.add_page()
    #pdf.header(header)

    pdf.chapter_body(text)
    pdf.output(pdf_file)

# Beispielaufruf
#txt_to_pdf('extracted.txt', 'output.pdf')