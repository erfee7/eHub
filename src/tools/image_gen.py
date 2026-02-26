# src/tools/image_gen.py

import mcp.types as types
from src.config import settings
from src.providers.openrouter import generate_image_via_openrouter

# The definition that tells the LLM what this tool does and what parameters it accepts
IMAGE_GEN_TOOL = types.Tool(
    name="generate_image",
    description=(
        "Generates an image based on a text prompt. "
        f"Default to using the '{settings.default_image_model}' model. "
        "Only specify the 'model' parameter if the user explicitly asks for a different specific image model."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The detailed visual description of the image the user wants to generate."
            },
            "model": {
                "type": "string",
                "description": f"The explicitly requested OpenRouter image model. Leave blank to use default."
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