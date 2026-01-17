import requests
import re

class OllamaPromptBooster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "The prompt you want to enhance using the selected local LLM."
                }),
                "use_llm": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "If disabled, the prompt will pass through unchanged."
                }),
                "model": (
                    ["zephyr:7b-beta", "deepseek-r1:8b", "llama3.2:latest", "mistral:latest", "gpt-oss:20b", "ministral-3:latest"],
                        {
                            "default": "zephyr:7b-beta",
                            "tooltip": "Choose which LLM to use for enhancement. No API key needed."
                        }
                        ),
                "cleanup_output": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Remove extra formatting, <think> tags, or LLM commentary from output."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "boost"
    CATEGORY = "OllamaTools"
    CLASS_NAME = "🧠 Prompt Booster"

    def boost(self, prompt, use_llm, model, cleanup_output):
        if not use_llm:
            return (prompt,)

        base_instruction = "Improve this prompt for a text-to-image AI model. Focus on clarity and visual detail. Respond in english language. Return only the improved prompt without additional information"

        payload = {
            "model": model,
            "prompt": f"{base_instruction}\n\n{prompt}",
            "stream": False
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
        return text.strip().strip('"').strip()

NODE_CLASS_MAPPINGS = {
    "OllamaPromptBooster": OllamaPromptBooster
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaPromptBooster": "🧠 Prompt Booster"
}
