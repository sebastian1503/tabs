import subprocess
import re
import tempfile
import os
from txt_to_pdf import txt_to_pdf
import os
import pdfkit
import requests
import html

def text_to_pdf_pdfkit(text, output_file):
    with open ("text.html", "w") as output:
        text.replace("\n", "<br>")
        output.write(text)

    pdfkit.from_file(text, output_path=output_file)


def fetch_website_content_curl(url):
    curl_command = ['curl', '-s', url]  # -s für Silent Mode
    result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Fehler beim Abrufen der Webseite: {result.stderr}")
    return result.stdout

def fetch_website_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Fehler beim Abrufen der Webseite: {response.status_code}")
    
    return response.text

def extract_content(html):
    pattern = r'<div class="js-store".*;content&quot;:&quot;(.*)\[/tab\]&quot;'
    match = re.search(pattern, html)
    if match:
        return match.group(1)
    else:
        raise Exception("No content found.")

def extract_title(html):
    pattern = r'song_name&quot;:&quot;(\w+)&quot;'
    match = re.search(pattern, html)
    if match:
        return match.group(1)
    else:
        raise Exception("No content found.")

def clean_content(content):
    content = content.replace('\\r\\n', '\n ')
    content = content.replace('[ch]', '')
    content = content.replace('[/ch]', '')
    content = content.replace('[tab]', '')
    content = content.replace('[/tab]', '')
    content = content.replace('&', '')
    content = content.replace('#', '')
    content = content.replace('\\quot', '')
    content = content.replace('\\&quot;', '')
    content = content.replace('039;', '\'')
    content = html.unescape(content)
    return content

def escape_latex(content):
    latex_special_characters = {
        '%': '\\%', '$': '\\$', '&': '\\&', '#': '\\#', '_': '\\_',
        '{': '\\{', '}': '\\}', '~': '\\textasciitilde', '^': '\\textasciicircum',
        '\\': '\\textbackslash', '\n': ' '  # Ersetzt neue Zeilen mit einem Leerzeichen (optional anpassbar)
    }
    
    for char, escaped in latex_special_characters.items():
        content = content.replace(char, escaped)
    
    return content

def create_latex_pdf(content):
    
        tex_file_path = os.path.join(os.path.curdir, 'document.tex')
        
        # Erstelle LaTeX-Dokument
        latex_content = f"""
        \\documentclass{{article}}
        \\usepackage[utf8]{{inputenc}}
        \\begin{{document}}
        \\section*{{Extrahierter Inhalt}}
        {content}
        \\end{{document}}
        """
        
        with open(tex_file_path, 'w', encoding='utf-8') as tex_file:
            tex_file.write(latex_content)
        
        result = subprocess.run(['pdflatex', tex_file_path], cwd=os.path.curdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Fehler bei der LaTeX-Kompilierung: {result.stderr}")
        
        pdf_file_path = os.path.join(os.path.curdir, 'document.pdf')
        return pdf_file_path

def main():
    url = 'https://tabs.ultimate-guitar.com/tab/coldplay/viva-la-vida-chords-675427'  # Ersetze dies durch die gewünschte URL
    url = 'https://tabs.ultimate-guitar.com/tab/coldplay/the-scientist-chords-50712'
    try:
        html_content = fetch_website_content(url)
        
        title = extract_title(html_content)

        extracted_content = extract_content(html_content)
        
        cleaned_content = clean_content(extracted_content)

        #cleaned_content = escape_latex(cleaned_content)
        
        #pdf_file_path = create_latex_pdf(cleaned_content)
        output_name = f"{"_".join(title.split(" "))}"
        with open (output_name + '.txt', 'w',  encoding='utf-8') as file:
            file.write(cleaned_content)
            
        #pdf_file_path = "Test.pdf"
        txt_to_pdf(cleaned_content, output_name + ".pdf")
        
        print(f"PDF wurde erfolgreich erstellt:")
    
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
