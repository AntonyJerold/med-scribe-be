import httpx
import json
import re
from typing import Dict, Any
from configs.constants import OLLAMA_URL, MODEL, SYSTEM_PROMPT



def clean_llm_output(text: str) -> str:
    """
    Remove code block markers and extra whitespace from LLM output.
    """
    # Nomalize LLM Output
    cleaned = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    return cleaned.strip()



def extract_json(text: str) -> str:
    # Extract JSON from LLM
    try:
        # Match {...} from text
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return match.group(0)
        return text  # fallback: return original text
    except Exception:
        return text



async def call_ollama(text: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": text},
                    ],
                    "options": {"temperature": 0}
                }
            )

        if response.status_code != 200:
            return {
                "error": "API request failed",
                "details": response.text
            }

        data = response.json()
        content = data.get("message", {}).get("content", "")

        if not content:
            return {"error": "Empty response from model"}

        cleaned = clean_llm_output(content)
        json_text = extract_json(cleaned)

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response",
                "raw": json_text
            }

    except httpx.RequestError as e:
        return {
            "error": "Connection error",
            "details": str(e)
        }

    except Exception as e:
        return {
            "error": "Unexpected error",
            "details": str(e)
        }