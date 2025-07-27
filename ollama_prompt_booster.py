import requests
import json

class OllamaPromptBooster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "use_llm": (["yes", "no"], {"default": "yes"}),
                "model": (
                    ["zephyr:7b-beta", "deepseek-r1:8b", "llama3.2:latest", "mistral:latest"],
                    {"default": "zephyr:7b-beta"}
                ),
                "cleanup_output": (["yes", "no"], {"default": "yes"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "boost"
    CATEGORY = "OllamaTools"

    # 🎈 Tooltip-Infos für bessere Benutzerfreundlichkeit
    UI_CONFIG = {
        "prompt": {
            "tooltip": "The original prompt you want to enhance. Can be simple or detailed."
        },
        "use_llm": {
            "tooltip": "Choose 'yes' to let the LLM improve your prompt. 'No' returns your input unchanged."
        },
        "model": {
            "tooltip": "Pick the LLM model used to boost your prompt. Some models are more verbose than others."
        },
        "cleanup_output": {
            "tooltip": "Removes <think> tags or excessive commentary to keep only the usable prompt."
        },
    }

    def boost(self, prompt, use_llm, model, cleanup_output):
        if use_llm == "no":
            return (prompt,)

        url = "http://localhost:11434/api/generate"
        system_prompt = "Improve this prompt for a text-to-image model. Only return the enhanced version. No comments, no explanations."

        payload = {
            "model": model,
            "prompt": f"{system_prompt}\n\n{prompt}",
            "stream": False
        }

        try:
            response = requests.post(url, json=payload)
            result = response.json()["response"]
        except Exception as e:
            result = f"[ERROR contacting Ollama: {e}]"

        if cleanup_output == "yes":
            result = self._cleanup_response(result)

        return (result,)

    def _cleanup_response(self, text):
        import re
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = text.strip().strip('"').strip()
        return text