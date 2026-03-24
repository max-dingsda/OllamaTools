import json
import re
import requests


class OllamaPromptBooster:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "use_llm": ("BOOLEAN", {"default": True}),
                "model": (
                    [
                        "nemotron-mini:4b",
                        "mistral:latest",
                        "zephyr:latest",
                        "llama3.2:latest",
                        "deepseek-r1:8b",
                        "ministral-3:latest",
                        "gpt-oss-fast:latest",
                    ],
                    {"default": "nemotron-mini:4b"},
                ),
                "cleanup_output": ("BOOLEAN", {"default": True}),
                "temperature": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.5, "step": 0.05}),
                "timeout_sec": ("INT", {"default": 120, "min": 5, "max": 600, "step": 5}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt", "constraints")
    FUNCTION = "boost"
    CATEGORY = "OllamaTools"
    CLASS_NAME = "?? Prompt Compiler (pos/neg/constraints)"

    def boost(self, prompt, use_llm, model, cleanup_output, temperature, timeout_sec):
        if not use_llm:
            return (prompt, "", "")

        # Triple-quoted to avoid any escaping/unterminated-string issues.
        base_instruction = r"""You are a STRICT prompt compiler for Stable Diffusion XL (SDXL).
Your task is to transform the user's idea into explicit, concrete visual instructions for a single image.

You MUST output EXACTLY three fields:
- positive: what should be visible as a detailed visual scene
- negative: a STRICT comma- or semicolon-separated list of things to suppress. Use ONLY nouns or short noun phrases (no verbs, no full sentences, no negations like "no/not/without/avoid"). Prefer common AI artifacts.
- constraints: short VISUAL/SPATIAL/NUMERICAL rules only (composition, counts, distances, framing)

IMPORTANT RULES:
- Do NOT copy the user's text verbatim; re-express it visually.
- The positive field MUST describe a complete scene that could be depicted in one image:
  subject + environment + time/lighting + viewpoint/framing (e.g., wide/medium/close, angle).
- You MUST expand short/abstract input into a rich, concrete scene.
- Do NOT add "photography advice" or meta instructions (no color grading tips, no writing rules).
  BUT you MAY include neutral visual descriptors like "soft morning light", "overcast daylight", "warm interior glow"
  and simple framing terms like "wide shot", "medium shot", "close-up", "low angle", "eye level".

CONSTRAINTS RULES (VERY IMPORTANT):
- Constraints are NOT a negative prompt.
- Constraints should control layout/geometry only, e.g.:
  "single main subject"; "centered composition"; "house fully visible"; "medium distance"; "horizon in upper third".
- Do NOT list content bans like "no people, no sky, no grass" unless the user explicitly asked to exclude them.

OUTPUT QUALITY RULES:
- positive MUST be at least 35 words and include:
  subject, environment, time/lighting, and viewpoint/framing.
- constraints MUST contain at least 3 short items.
- negative MUST contain at least 10 common artifact items (e.g., blurry, watermark, text, jpeg artifacts, deformed, extra limbs, bad anatomy, bad hands, lowres, oversaturated).

OUTPUT FORMAT RULES:
- Output ONLY valid JSON.
- No markdown, no commentary, no extra keys.
- If a field is unknown, output an empty string.

Return exactly:
{"positive":"...","negative":"...","constraints":"..."}
"""

        payload = {
            "model": model,
            "prompt": f"{base_instruction}\nUSER_TEXT:\n{prompt}\n",
            "stream": False,
            # Ask Ollama to return JSON text (some models still wrap it in a string; we parse below).
            "format": "json",
            "options": {"temperature": float(temperature), "num_ctx": 2048},
        }

        try:
            r = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json=payload,
                timeout=int(timeout_sec),
            )
            r.raise_for_status()
            raw = r.json().get("response", "")
        except Exception as e:
            return (f"[OLLAMA ERROR] {e}", "", "")

        if cleanup_output:
            raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL | re.IGNORECASE).strip()

        obj = self._parse_json_safely(raw)
        if not obj:
            return (f"[LLM JSON PARSE ERROR]\n{raw}", "", "")

        positive = self._to_text(obj.get("positive"))
        negative = self._to_text(obj.get("negative"))
        constraints = self._to_text(obj.get("constraints"))

        # Hard defaults so we never return empty neg/constraints.
        if not negative:
            negative = (
                "low quality, blurry, bad anatomy, extra limbs, extra fingers, "
                "duplicate body, deformed hands, deformed face, text, watermark"
            )
        if not constraints:
            constraints = "single subject; action visible; environment visible"

        return (positive, negative, constraints)

    def _parse_json_safely(self, raw: str):
        # 1) Try direct
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass

        # 2) Try to extract first {...} block
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                obj = json.loads(m.group(0))
                if isinstance(obj, dict):
                    return obj
            except Exception:
                pass

        return None

    def _to_text(self, value) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, list):
            parts = []
            for item in value:
                if item is None:
                    continue
                if isinstance(item, str):
                    s = item.strip()
                    if s:
                        parts.append(s)
                else:
                    parts.append(str(item).strip())
            return "; ".join([p for p in parts if p])
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False).strip()
        return str(value).strip()


NODE_CLASS_MAPPINGS = {
    "OllamaPromptBooster": OllamaPromptBooster,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaPromptBooster": "?? Prompt Compiler (pos/neg/constraints)",
}
