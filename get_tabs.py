import subprocess
import re
import tempfile
import os
from txt_to_pdf import txt_to_pdf
import os
import pdfkit
import requests
import html
import numpy as np
from parse_html import TabParser

CHARACTERS_PER_LINE_AT_WRITING_SIZE_8 = 111
CHARACTERS_PER_LINE_AT_WRITING_SIZE_9 = 98
CHARACTERS_PER_LINE_AT_WRITING_SIZE_10 = 88
CHARACTERS_PER_LINE_AT_WRITING_SIZE_11 = 80
CHARACTERS_PER_LINE_AT_WRITING_SIZE_12 =74

LINES_PER_PAGE_AT_SPACING_3 = 81
LINES_PER_PAGE_AT_SPACING_4 = 60

CHARACTERS_PER_LINE = CHARACTERS_PER_LINE_AT_WRITING_SIZE_8
LINES_PER_PAGE = LINES_PER_PAGE_AT_SPACING_3





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
        return "no title"
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

def text_to_multicolumn(text):

    max_lines_per_page = LINES_PER_PAGE
    max_characters_per_page = CHARACTERS_PER_LINE
    min_v_dist = 0
    lines_in_list = text.split("\n")
    restlines = len(lines_in_list)
    returnlines = []
    while restlines > max_lines_per_page:
        max_length_first_block = np.max([len(i) for i in lines_in_list[0:max_lines_per_page]])
        restlines -= max_lines_per_page
        end_second_block = np.min([max_lines_per_page, restlines])
        max_length_second_block = np.max([len(i) for i in lines_in_list[max_lines_per_page:max_lines_per_page + end_second_block]])
        if (max_length_first_block + max_length_second_block + min_v_dist) < max_characters_per_page:
            min_size = max_length_first_block + min_v_dist
            for i in range(max_lines_per_page):
                if i < restlines:
                    fill_character = min_size - len(lines_in_list[i])
                    returnlines.append(lines_in_list[i] + fill_character * " " + lines_in_list[i+max_lines_per_page])
                else:
                    returnlines.append(lines_in_list[i])
            if restlines>max_lines_per_page:
                restlines-=max_lines_per_page
                lines_in_list = lines_in_list[2*max_lines_per_page:]
            else:
                restlines = 0
                lines_in_list = []
                    
    return "\n".join(returnlines) + "\n".join(lines_in_list)
    
    


def main():
    url = 'https://tabs.ultimate-guitar.com/tab/coldplay/viva-la-vida-chords-675427'  # Ersetze dies durch die gewünschte URL
    url = 'https://tabs.ultimate-guitar.com/tab/coldplay/the-scientist-chords-50712'
    url = "https://tabs.ultimate-guitar.com/tab/britney-spears/baby-one-more-time-chords-279810"
    url = "https://tabs.ultimate-guitar.com/tab/liquido/narcotic-chords-924106"
    #url = 'https://tabs.ultimate-guitar.com/tab/bryan-adams/summer-of-69-chords-843137'
    try:
        
        html_content = fetch_website_content(url)

        with open("debug.html", 'w',  encoding='utf-8') as file:
            file.write(html_content)
        
        tabParser = TabParser(html_content)

        title = tabParser.get_song_name()

        extracted_content = tabParser.get_tabs_content()
        
        cleaned_content = clean_content(extracted_content)
        
        cleaned_content = text_to_multicolumn(cleaned_content)

        #cleaned_content = escape_latex(cleaned_content)
        
        #pdf_file_path = create_latex_pdf(cleaned_content)
        output_folder = "out/"
        output_name = output_folder + f"{"_".join(title.split(" "))}"
        with open (output_name + '.txt', 'w',  encoding='utf-8') as file:
            file.write(cleaned_content)
            
        #pdf_file_path = "Test.pdf"
        txt_to_pdf(cleaned_content, title, output_name + ".pdf")
        
        print(f"PDF {title} wurde erfolgreich erstellt:")
    
    except Exception as e:
        print(f"Fehler: {e}")


def testPDF():
    
    title = "test"
    cleaned_content = ""
    for i in range(200):
        num = f"{i}"
        cleaned_content += num + (CHARACTERS_PER_LINE - len(num))*"X"
    txt_to_pdf(cleaned_content, title, "out/" + title + ".pdf")

if __name__ == "__main__":
    #testPDF()
    main()
