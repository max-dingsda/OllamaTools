class PromptStylist:
    @classmethod
    def INPUT_TYPES(cls):
        styles = [
            "None",
            "Oil Painting",
            "Photography",
            "Comic Drawing",
            "Anime Drawing",
            "Commercial",
        ]
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "The prompt to which a visual style should be applied"
                }),
                "style_tone": (styles, {
                    "default": "None",
                    "tooltip": "Choose the visual style for the resulting image"
                }),
                "nsfw": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "If enabled, uses an uncensored NSFW variant of the style"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("styled_prompt",)
    FUNCTION = "apply_style"
    CATEGORY = "OllamaTools"
    CLASS_NAME = "🎨 Prompt Stylist"

    def apply_style(self, prompt, style_tone, nsfw):
        sfw_styles = {
            "Oil Painting": "style: oil painting, textured brushstrokes, painterly composition",
            "Photography": "style: photography, realistic lighting, lens blur, shallow depth of field",
            "Comic Drawing": "style: comic book, flat colors, strong lines, dramatic composition",
            "Anime Drawing": "style: anime, clean lines, cel shading, vibrant colors",
            "Commercial": "style: commercial poster, bold layout, text overlay, high contrast"
        }

        nsfw_styles = {
            "Oil Painting": "style: erotic oil painting, sensual brushwork, artistic nudity",
            "Photography": "style: glamour photography, boudoir lighting, intimate setting",
            "Comic Drawing": "style: erotic comic, bold line art, exaggerated curves, explicit expression",
            "Anime Drawing": "style: lewd anime, fantasy proportions, soft lighting, exposed poses",
            "Commercial": "style: provocative ad, seductive message, glossy layout"
        }

        if style_tone == "None":
            return (prompt,)

        style_dict = nsfw_styles if nsfw else sfw_styles
        if style_tone in style_dict:
            styled_prompt = f"{style_dict[style_tone]}\n{prompt}"
        else:
            styled_prompt = prompt

        return (styled_prompt,)


NODE_CLASS_MAPPINGS = {
    "PromptStylist": PromptStylist
}
