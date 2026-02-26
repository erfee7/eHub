# src/providers/openrouter.py

import httpx
from src.config import settings

async def generate_image_via_openrouter(prompt: str, model: str) -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image"]
    }
    
    # Generate image. Timeout set higher (60s) as image generation can take time
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
    try:
        # Extract the Base64 image URL string from OpenRouter standard response
        b64_url = data["choices"][0]["message"]["images"][0]["image_url"]["url"]
        return _parse_data_url(b64_url)
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response format from OpenRouter: {data}") from e

def _parse_data_url(data_url: str) -> dict:
    """Parses 'data:image/png;base64,iVBO...' into its components."""
    if not data_url.startswith("data:"):
        # Fallback if the provider forgets the prefix
        return {"mime_type": "image/png", "data": data_url}
        
    header, b64_data = data_url.split(",", 1)
    mime_type = header.split(";")[0][5:] # Extract 'image/png'
    return {"mime_type": mime_type, "data": b64_data}