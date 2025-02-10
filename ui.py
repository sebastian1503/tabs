import tkinter as tk
from tkinter import filedialog
from get_tabs import crawl_tabs

def get_pdf():
    url = url_entry.get()
    transpose_value = transpose_entry.get()
    save_path = save_path_entry.get()
    
    if not url or not save_path:
        status_label.config(text="Bitte alle Felder ausfüllen!", fg="red")
        return
    
    # Hier kann die Logik zum Abrufen und Speichern der PDF-Datei implementiert werden
    print(f"URL: {url}, Transpose: {transpose_value}, Save Path: {save_path}")
    crawl_tabs(url, int(transpose_value), save_path)
    
    # Lösche nur das URL-Feld
    url_entry.delete(0, tk.END)
    status_label.config(text="PDF generiert!", fg="green")

def browse_path():
    folder_selected = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, folder_selected)

root = tk.Tk()
root.title("Chords Crawler")
root.geometry("400x200")

tk.Label(root, text="ultimate-guitar URL eingeben:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="Transponiere um:").pack()
transpose_entry = tk.Entry(root, width=10)
transpose_entry.pack()

tk.Label(root, text="Speicherpfad:").pack()
save_path_entry = tk.Entry(root, width=50)
save_path_entry.pack()
browse_button = tk.Button(root, text="Durchsuchen", command=browse_path)
browse_button.pack()

get_pdf_button = tk.Button(root, text="Get PDF", command=get_pdf)
get_pdf_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
