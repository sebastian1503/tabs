from flask import Flask, request, send_file, jsonify
from get_tabs import crawl_tabs
import os
import tempfile

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        url = data.get("url")
        transpose = int(data.get("transpose", 0))

        if not url:
            return jsonify({"error": "Missing URL"}), 400

        tmpdir = tempfile.mkdtemp()

        # crawl_tabs anpassen: liefert jetzt (pdf_path, title) zurück
        pdf_path, title = crawl_tabs(url, transpose, tmpdir, german=False)

        return send_file(pdf_path,
                         download_name=f"{title}.pdf",
                         as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Backend is running."
