from .ollama_prompt_booster import NODE_CLASS_MAPPINGS as booster_nodes
from .ollama_pic_description import NODE_CLASS_MAPPINGS as describer_nodes

NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(booster_nodes)
NODE_CLASS_MAPPINGS.update(describer_nodes)

NODE_DISPLAY_NAME_MAPPINGS = {
    key: value.CLASS_NAME for key, value in NODE_CLASS_MAPPINGS.items()
}