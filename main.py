# main.py
import os
import tempfile
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)


# add "/" for health check
@app.get("/")
def health_check():
    print("Health Check! Ok!")
    return "OK"


@app.route("/download", methods=["POST"])
def download_html():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = download_html_by_singlefile(url)

    if result:
        with open(result, "r", encoding="utf-8") as f:
            content = f.read()
        os.remove(result)  # 清理临时文件
        return jsonify({"content": content})
    else:
        return jsonify({"error": "Failed to download HTML"}), 500


def download_html_by_singlefile(url: str) -> str:
    filename = tempfile.mktemp(suffix=".html")
    print(f"download {url} to {filename}")
    cmds = ["single-file", url, "--output", filename]
    try:
        subprocess.run(cmds, check=True)
        return filename
    except Exception as e:
        print(f"failed to download html by single-file: {e}")
        return ""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
