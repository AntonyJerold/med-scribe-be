# Modules Import
from fastapi import FastAPI, Query, HTTPException
from pathlib import Path
import base64

from utils.transcriber import transcribe
from utils.ollama_soap_client import call_ollama
from utils.helpers import save_json
from configs.constants import DEFAULT_FILE_PATH, DEFAULT_FILE

# Initialize FastAPI app
app = FastAPI()

BASE_DIR = Path(__file__).parent
DEFAULT_FILE = BASE_DIR / DEFAULT_FILE_PATH / DEFAULT_FILE

# Route to GET SOAP transcription
@app.get("/soap-transcribe")
async def transcribe_audio_to_soap(filename: str | None = Query(None, description="Optional audio file name")):
    try:
        # Use provided filename if exists, else default file
        file_path = (BASE_DIR / "resources" / Path(filename).name) if filename else DEFAULT_FILE
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File '{filename or DEFAULT_FILE.name}' not found")

        # Read and encode file
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        
        # Transcribe audio to text
        transcription_result = await transcribe(encoded, filename or DEFAULT_FILE.name) or ""

        # convert text to SOAP format
        soap = await call_ollama(transcription_result) or ""

        # Define Results
        results = {   
            'transcript': transcription_result,
            'SOAP': soap
        }

        # Save results to Results folder
        save_json(results)

        # Return results
        return results        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))