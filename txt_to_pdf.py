from fpdf import FPDF

# PDF-Klasse erstellen
class PDF(FPDF):
    def header(self):
        self.set_font('Courier', '', 12)  # Monospaced Font verwenden
        self.cell(0, 10, 'Gitarrenakkorde zu PDF', align='C', ln=True)
        self.ln(10)  # Zeilenumbruch

    def chapter_body(self, body):
        self.set_font('Courier', '', 12)  # Monospaced Font für Text
        self.multi_cell(0, 5, body)  # Multi_Cell sorgt für Textumbruch
        self.ln()
# Funktion zum Umwandeln von TXT zu PDF
def txt_to_pdf(text, pdf_file):
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_body(text)
    pdf.output(pdf_file)

# Beispielaufruf
#txt_to_pdf('extracted.txt', 'output.pdf')