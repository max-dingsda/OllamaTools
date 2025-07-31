import requests
import json

class OllamaPromptBooster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "tooltip": "The original prompt you want to enhance. Can be simple or detailed."
                    }
                ),
                "use_llm": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Enable this to improve your prompt with the selected LLM."
                    }
                ),
                "model": (
                    ["zephyr:7b-beta", "deepseek-r1:8b", "llama3.2:latest", "mistral:latest"],
                    {
                        "default": "zephyr:7b-beta",
                        "tooltip": "Choose which LLM to use for prompt enhancement. Some are more verbose than others."
                    }
                ),
                "cleanup_output": (
                    "BOOLEAN",
                    {
                        "default": True,
                        "tooltip": "Removes unnecessary text like <think> tags or explanations from the LLM output."
                    }
                ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "boost"
    CATEGORY = "OllamaTools"
    CLASS_NAME = "Ollama Prompt Booster"

    def boost(self, prompt, use_llm, model, cleanup_output):
        if not use_llm:
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

        if cleanup_output:
            result = self._cleanup_response(result)

        return (result,)

    def _cleanup_response(self, text):
        import re
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = text.strip().strip('"').strip()
        return text

NODE_CLASS_MAPPINGS = {
    "OllamaPromptBooster": OllamaPromptBooster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaPromptBooster": "🧠 Prompt Booster"
}
