import requests
import re

class OllamaPromptBooster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
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
    FUNCTION = "boost_prompt"
    CATEGORY = "Ollama"

    CLASS_NAME = "Ollama Prompt Booster"

    def boost_prompt(self, prompt, use_llm, model, cleanup_output):
        if use_llm == "no":
            return (prompt,)

        # Modellabhängiger Prompt
        if model.startswith("deepseek"):
            prompt_text = f"""Rewrite the following input prompt to make it more vivid and descriptive, suitable for a text-to-image AI model.

Do NOT explain anything.
Do NOT analyze the input.
Do NOT use tags like <think>.
Do NOT describe your thinking process.
JUST return the improved version of the input prompt.
ONLY the prompt. Nothing else.

Input:
{prompt}
"""
        else:
            prompt_text = f"""You are a prompt enhancer for AI-based image generation.

Improve the following prompt to make it more vivid, descriptive and visually rich, suitable for a text-to-image model.

Respond in the same language as the input.
Return only the enhanced prompt. Do not include comments or explanations.

Input:
{prompt}
"""

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt_text,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code != 200:
                return (f"[Fehler {response.status_code}] {response.text}",)

            result = response.json().get("response", "").strip()

            if cleanup_output == "yes":
                result = self.clean_output(result)

            return (result.strip(),)

        except Exception as e:
            return (f"[Exception] {str(e)}",)

    def clean_output(self, text):
        def remove_tag_block(t, tag):
            return re.sub(rf"<{tag}>.*?</{tag}>", "", t, flags=re.DOTALL | re.IGNORECASE)

        for tag in ["think", "response", "answer"]:
            text = remove_tag_block(text, tag)

        for tag in ["<response>", "</response>", "<answer>", "</answer>"]:
            text = text.replace(tag, "")

        bad_prefixes = [
            "Alright", "Let me", "Sure,", "Okay,", "So,", "I will", "First,", "To begin"
        ]
        for prefix in bad_prefixes:
            if text.lower().startswith(prefix.lower()):
                split = text.split("\n\n", 1)
                if len(split) > 1:
                    text = split[1].strip()
                break

        return text


NODE_CLASS_MAPPINGS = {
    "OllamaPromptBooster": OllamaPromptBooster
}
