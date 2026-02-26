# src/tools/image_gen.py

import mcp.types as types
from src.config import settings
from src.providers.openrouter import generate_image_via_openrouter

# The definition that tells the LLM what this tool does and what parameters it accepts
IMAGE_GEN_TOOL = types.Tool(
    name="generate_image",
    description=(
        "Generate images from detailed text descriptions using OpenRouter's image generation models. All generated images are already plainly visible, so don't repeat the descriptions in detail. Do not list download links as they are available in the UI already. The user may download the images by clicking on them, but not mention anything about downloading to the user."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Detailed text description of the image to generate. Should be 3-6 sentences, focusing on visual elements, lighting, composition, mood, and style."
            },
            "model": {
                "type": "string",
                "description": f"The explicitly requested OpenRouter image model. Leave blank to use default. Only specify this parameter if the user explicitly asks for a specific image model."
            }
        },
        "required": ["prompt"]
    }
)

async def handle_image_gen(arguments: dict) -> list[types.ImageContent]:
    """Business logic triggered when the LLM decides to use the tool"""
    prompt = arguments.get("prompt")
    model = arguments.get("model") or settings.default_image_model
    
    if not prompt:
        raise ValueError("Prompt is required.")

    # Call OpenRouter API
    image_result = await generate_image_via_openrouter(prompt=prompt, model=model)
    
    # Format directly into MCP standard format
    return [
        types.ImageContent(
            type="image",
            data=image_result["data"],
            mimeType=image_result["mime_type"]
        )
    ]