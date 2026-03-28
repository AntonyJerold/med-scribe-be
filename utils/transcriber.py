import io
import base64
from pathlib import Path
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

async def transcribe(audio_input: bytes | str, filename: str) -> dict:
    try:
        # Validate file type
        if not filename or Path(filename).suffix.lower() != ".mp3":
            return {"error": "Only .mp3 files are supported"}

        # Decode base64 if needed
        if isinstance(audio_input, str):
            try:
                audio_input = base64.b64decode(audio_input)
            except Exception:
                return {"error": "Invalid base64 audio input"}

        # Validate audio bytes
        if not isinstance(audio_input, (bytes, bytearray)) or len(audio_input) == 0:
            return {"error": "Empty or invalid audio input"}

        # Transcription
        try:
            segments_iter, _ = model.transcribe(
                io.BytesIO(audio_input),
                language="en",
                beam_size=5,
                vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 500},
            )
        except Exception as e:
            return {"error": f"Transcription failed: {str(e)}"}

        # Extract only text
        try:
            transcript = " ".join(
                seg.text.strip() for seg in segments_iter if seg.text
            ).strip()

        except Exception:
            return {"error": "Failed while processing transcription segments"}

        return transcript

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}