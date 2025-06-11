import logging
import os
import subprocess
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔧 FFmpeg test Function triggered.")

    ffmpeg_path = os.path.join(os.path.dirname(__file__), "../bin/ffmpeg")
    try:
        result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("✅ FFmpeg is available and working.")
            return func.HttpResponse("✅ FFmpeg is available\n" + result.stdout)
        else:
            logging.error("❌ FFmpeg failed: " + result.stderr)
            return func.HttpResponse("❌ FFmpeg error\n" + result.stderr, status_code=500)
    except Exception as e:
        logging.error("❌ Exception occurred: " + str(e))
        return func.HttpResponse("❌ Exception occurred\n" + str(e), status_code=500)
