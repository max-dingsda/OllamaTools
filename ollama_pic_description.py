import base64
import requests
import re
import numpy as np
from io import BytesIO
from PIL import Image

class OllamaPicDescriber:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (
                    ["llava:latest", "moondream:latest"],
                    {"default": "llava:latest"}
                ),
                "style": (
                    ["neutral", "cinematic", "poetic", "erotic", "technical", "nsfw"],
                    {"default": "neutral"}
                ),
                "prompt": ("STRING", {"default": "Describe this image"}),
                "cleanup_output": (["yes", "no"], {"default": "yes"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "describe"
    CATEGORY = "Ollama"

    CLASS_NAME = "Ollama PIC Describer"

    def describe(self, image, model, style, prompt, cleanup_output):
        img_array = image[0].cpu().numpy()
        img_uint8 = (img_array * 255).clip(0, 255).astype("uint8")
        pil_image = Image.fromarray(img_uint8)

        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        style_prompt = self.style_to_prompt(style)
        full_prompt = f"{prompt.strip()} {style_prompt}".strip()

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "images": [img_str],
                    "stream": False
                },
                timeout=60
            )

            if response.status_code != 200:
                return (f"[Fehler {response.status_code}] {response.text}",)

            result = response.json().get("response", "").strip()

            if cleanup_output == "yes":
                result = self.clean_output(result)

            return (result,)

        except Exception as e:
            return (f"[Exception] {str(e)}",)

    def style_to_prompt(self, style):
        prompts = {
            "neutral": "",
            "cinematic": "Use a cinematic tone, focusing on atmosphere and visual storytelling.",
            "poetic": "Use poetic, metaphor-rich language.",
            "erotic": "Add sensual undertones, without being explicit.",
            "technical": "Describe in a dry, factual, and precise tone.",
            "nsfw": "Be explicit and unfiltered. Use uncensored language to describe all visible erotic elements.",
        }
        return prompts.get(style, "")

    def clean_output(self, text):
        def remove_tag_block(t, tag):
            return re.sub(rf"<{tag}>.*?</{tag}>", "", t, flags=re.DOTALL | re.IGNORECASE)

        for tag in ["think", "response", "answer"]:
            text = remove_tag_block(text, tag)

        for tag in ["<response>", "</response>", "<answer>", "</answer>"]:
            text = text.replace(tag, "")

        bad_prefixes = [
            "As an AI", "I see", "The image shows", "Let me explain", "In the image"
        ]
        for prefix in bad_prefixes:
            if text.lower().startswith(prefix.lower()):
                split = text.split("\n\n", 1)
                if len(split) > 1:
                    text = split[1].strip()
                break

        return text


NODE_CLASS_MAPPINGS = {
    "OllamaPicDescriber": OllamaPicDescriber
}
