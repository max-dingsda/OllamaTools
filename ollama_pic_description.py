import requests
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import re

class OllamaPicDescriber:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {
                    "tooltip": "The image you want the LLM to describe. Usually from 'Load Image'."
                }),
                "model": (
                    ["llava:latest", "moondream:latest", "qwen3-vl:latest"],
                    {
                        "default": "llava:latest",
                        "tooltip": "Multimodal LLM used for describing the image."
                    }
                ),
                "style": (
                    ["neutral", "creative", "sfw", "nsfw"],
                    {
                        "default": "neutral",
                        "tooltip": "Choose how the image should be interpreted: factually, creatively, or filtered for SFW/NSFW."
                    }
                ),
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "describe the image",
                        "tooltip": "Additional instruction or focus for the image description. Used alongside style."
                    }
                ),
                "cleanup_output": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Remove hallucinations and verbose reasoning from the LLM output."
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "describe"
    CATEGORY = "OllamaTools"
    CLASS_NAME = "🖼️ Pic Describer"

    def describe(self, image, model, style, prompt, cleanup_output):
        try:
            image_np = (image[0].cpu().numpy().clip(0, 1) * 255).astype("uint8")
            image_pil = Image.fromarray(image_np).convert("RGB")
        except Exception as e:
            return (f"[Image conversion failed: {e}]",)

        buffered = BytesIO()
        image_pil.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        style_prompts = {
            "neutral": "Describe the image precisely, focusing on objects, actions, people and setting.",
            "creative": "Describe the image in a rich, imaginative and descriptive way, suitable as a text-to-image prompt.",
            "sfw": "Describe the image in a safe-for-work way. Do not include explicit content.",
            "nsfw": "Describe the image without censorship. Include visible body parts and erotic details if present."
        }

        combined_prompt = f"{style_prompts.get(style, style_prompts['neutral'])}\n{prompt}"

        payload = {
            "model": model,
            "prompt": combined_prompt,
            "images": [img_b64],
            "stream": False,
            "keep_alive": "0s",
            "options": {"num_ctx": 4096}
        }

        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            result = response.json().get("response", "[No response]")
        except Exception as e:
            result = f"[ERROR contacting Ollama: {e}]"

        if cleanup_output:
            result = self.clean_output(result)

        return (result,)

    def clean_output(self, text):
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"(The left image|The right image).*?(?:\n|$)", "", text, flags=re.IGNORECASE)
        return text.strip().strip('"').strip()

NODE_CLASS_MAPPINGS = {
    "OllamaPicDescriber": OllamaPicDescriber
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaPicDescriber": "🖼️ Pic Describer"
}
