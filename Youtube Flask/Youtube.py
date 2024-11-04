from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)  # Allow all CORS requests

cur_directory = os.getcwd()

@app.route('/download', methods=['POST'])
def download_video():
    link = request.form.get('link')

    if not link:
        return jsonify({"error": "No link provided"}), 400

    # Generate a unique filename using the first 15 characters of the sanitized link
    sanitized_link = link.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"video-{sanitized_link[:15]}.mp4"
    output_path = os.path.join(cur_directory, filename)

    youtube_dl_options = {
        "format": "b",
        "outtmpl": output_path  # Use outtmpl instead of out
    }

    try:
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
        return jsonify({"message": "Download complete", "filename": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
