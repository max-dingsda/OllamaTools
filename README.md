# 🧠 OllamaTools for ComfyUI

> *“To be honest, most LLM nodes in ComfyUI were just too complicated for me.  
> So I built the kind of tools I wish I had when I started.”*

ComfyUI has powerful capabilities for working with local LLMs via [Ollama](https://ollama.com), but many existing nodes are complex, poorly documented, or difficult to use for newcomers, or to be honest, people like me

**This project makes local LLMs easy to use for prompt enhancement and image captioning –**  
No API keys. No external tools. No headache.

---

## 🧩 Included Nodes

### 🔹 Ollama Prompt Booster

Improves a basic text prompt using a local language model like Zephyr or DeepSeek.  
Turns short ideas into more vivid, descriptive prompts for text-to-image generation.

✅ Supports the following models:
- `zephyr:7b-beta`
- `deepseek-r1:8b`
- `llama3.2:latest`
- `mistral:latest`

---

### 🔹 Ollama Pic Describer

Takes an image and returns a prompt-like description.  
Great for `img2img`, ControlNet reruns, prompt recovery, or inspiration.  
Supports style options like `cinematic`, `poetic`, or `nsfw`.

✅ Supports the following models:
- `llava:latest`
- `moondream:latest`

---

## 🚀 Examples

### ✏️ Prompt Booster

Input:
```text
woman on a balcony, sunset, elegant
```

Output:
```text
An elegant woman gazes over the cityscape from a golden-lit balcony, her dress flowing in the evening breeze…
```

---

### 🖼️ Pic Describer

Given this image:  
*(Insert image of woman on a couch)*

Returns a prompt like:
```text
A beautiful woman lounges barefoot on a white sofa, her shirt loose and airy, lit by soft studio lighting…
```

---

## 💻 Installation

1. Install [Ollama](https://ollama.com) and make sure it's running locally
2. Clone this repo into your `ComfyUI/custom_nodes` folder:

```bash
git clone https://github.com/YOURNAME/ComfyUI-OllamaTools.git
```

3. (Optional) Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Launch ComfyUI and start building!

---

## 🔧 Model Setup

You can pull the models you need with:

```bash
ollama pull zephyr:7b-beta
ollama pull deepseek-r1:8b
ollama pull llava:latest
ollama pull moondream:latest
```

Only models you're using need to be installed.

---

## 🧠 Requirements

- Python 3.10+
- ComfyUI
- Ollama (running locally)
- Python libraries:
  - `requests`
  - `Pillow`

---

## 🪪 License

MIT – use freely, contribute gladly, no need to pretend you wrote it 😉

---

## 💬 About

This project was built out of necessity – and some self-deprecating humor.  
I wanted LLM features that "just work" inside ComfyUI.

If you're the same: welcome aboard.
