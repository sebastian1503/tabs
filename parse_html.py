from bs4 import BeautifulSoup
import json
import html
import re


class TabParser:
    def __init__(self, html_content):
        self.parsed_data = None
        soup = BeautifulSoup(html_content, "html.parser")

        # Daten aus dem "data-content"-Attribut extrahieren
        data_content = soup.find("div", class_="js-store")["data-content"]

        # HTML-Entities decodieren
        decoded_data = html.unescape(data_content)

        # Unerlaubte Steuerzeichen entfernen
        cleaned_data = re.sub(r"[\x00-\x1F\x7F]", "", decoded_data)

        try:
            # JSON parsen
            self.parsed_data = json.loads(cleaned_data)
        except json.JSONDecodeError as e:
            print("JSON Fehler:", e)
            print("Fehlerhafte Daten:", cleaned_data[:500])  # Zeigt einen Ausschnitt 

    def get_artist_name(self):
        try:
            return self.parsed_data['store']['page']['data']['tab']['artist_name']
        except Exception as e:
            print(e)
            return "artist not known"
    def get_song_name(self):
        try:
            return self.parsed_data['store']['page']['data']['tab']['song_name']
        except Exception as e:
            print(e)
            return "song name not known"
        
    
    def get_tabs_content(self):
        try:
            return self.parsed_data['store']['page']['data']['tab_view']['wiki_tab']['content']
        except Exception as e:
            print(e)
            return "null"
