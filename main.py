import os
import tempfile
import asyncio
from pathlib import Path
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from loguru import logger
from typing import Optional

app = Flask(__name__)


def get_singlefile_path_from_env() -> str:
    # 直接返回 'single-file'，因為它應該在 PATH 中
    return "single-file"


async def singlefile_download(url: str, cookies_file: Optional[str] = None) -> str:
    logger.info("Downloading HTML by SingleFile: {}", url)

    filename = tempfile.mktemp(suffix=".html")
    singlefile_path = get_singlefile_path_from_env()

    # 指定 Chromium 的可執行路徑
    chromium_path = "/usr/bin/chromium"

    cmds = [
        singlefile_path,
        "--browser-executable-path",
        chromium_path,
        "--filename-conflict-action",
        "overwrite",
        url,
        filename,
    ]

    if cookies_file is not None:
        if not Path(cookies_file).exists():
            raise FileNotFoundError("cookies file not found")

        cmds += [
            "--browser-cookies-file",
            cookies_file,
        ]

    try:
        process = await asyncio.create_subprocess_exec(
            *cmds, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error("SingleFile failed with error: {}", stderr.decode())
            return ""

        logger.info("SingleFile output: {}", stdout.decode())
        return filename
    except Exception as e:
        logger.error("Failed to execute SingleFile: {}", e)
        return ""


async def load_singlefile_html(url: str) -> str:
    f = await singlefile_download(url)

    with open(f, "rb") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        text = soup.get_text(strip=True)
    os.remove(f)  # 清理临时文件
    return text


@app.route("/download", methods=["POST"])
async def download_html():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify(error="URL is required"), 400

    try:
        content = await load_singlefile_html(url)
        # 使用關鍵字參數來構建 JSON 響應
        return jsonify(content=content), 200
    except Exception as e:
        logger.error("Failed to download HTML: {}", e)
        return jsonify(error="Failed to download HTML"), 500


# Health check endpoint
@app.route("/", methods=["GET"])
def health_check():
    logger.info("Health Check! Ok!")
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
