
import logging
import azure.functions as func
import os
import tempfile
import subprocess
import json
from pathlib import Path

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔧 Auphonic-style function triggered (Flex version).")

    preset = req.form.get("preset")
    if not preset:
        return func.HttpResponse("❌ 'preset' parameter missing.", status_code=400)

    file = req.files.get("file")
    if not file:
        return func.HttpResponse("❌ 'file' parameter missing.", status_code=400)

    # Save uploaded file
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    file.save(tmp_input.name)
    logging.info(f"📦 Saved input audio to {tmp_input.name}")

    # Load preset
    preset_path = Path("presets") / f"{preset}.json"
    if not preset_path.exists():
        return func.HttpResponse(f"❌ Preset '{preset}' not found.", status_code=404)

    with open(preset_path) as f:
        preset_data = json.load(f)

    background = preset_data.get("background")
    if not background or not os.path.exists(background):
        return func.HttpResponse(f"❌ Background file '{background}' not found.", status_code=500)

    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    try:
        cmd = [
            "ffmpeg",
            "-y", "-loop", "1", "-i", background,
            "-i", tmp_input.name,
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", output_path
        ]
        subprocess.run(cmd, check=True)
        logging.info("🎞️ Video created successfully.")
    except subprocess.CalledProcessError as e:
        return func.HttpResponse(f"❌ FFmpeg error: {e}", status_code=500)

    with open(output_path, "rb") as f:
        return func.HttpResponse(f.read(), mimetype="video/mp4")
