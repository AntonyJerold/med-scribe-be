# File config
DEFAULT_FILE = "sample_dictation.mp3"
DEFAULT_FILE_PATH = "resources"


# Ollama config
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral"

SYSTEM_PROMPT = """
You are a clinical assistant.

Convert the given text into SOAP format.

Return ONLY JSON:
{
  "Subjective": "...",
  "Objective": "...",
  "Assessment": "...",
  "Plan": "..."
}
"""