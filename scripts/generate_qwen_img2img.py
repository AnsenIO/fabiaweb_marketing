#!/usr/bin/env python3
"""Generate a FABIABox birthday image using Qwen-Image 2512 img2img via ComfyUI API."""
import argparse
import json
import os
import random
import sys
import time
import urllib.request
import urllib.error
import urllib.parse

COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "workflows", "qwen_image_2512_img2img.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "comfy_outputs")

PROMPT = (
    "Premium cinematic product photography of a compact dark gunmetal and copper mini PC workstation, "
    "the FABIABox, with dense vertical heatsink fins glowing warm amber from within, sitting on a polished "
    "wooden desk inside a luxurious high-tech penthouse office at night. Floor-to-ceiling windows show a "
    "softly blurred city skyline bokeh. Holographic blue data visualizations float in the background. "
    "A single lit birthday candle sits on top of the heatsink, warm flame reflecting on metal. "
    "Dramatic low-key cinematic lighting, photorealistic, 8K, shallow depth of field. No text, no logos, no typography, no words."
)

NEGATIVE = (
    "plastic, toy-like, empty heater, hollow grille, oversized, huge, cartoon, 3D render, cheap, "
    "glossy plastic, rubber, lightweight, distorted logo, blurry text, extra ports, USB-A, HDMI, "
    "audio jacks, watermark, text errors, low resolution, blurry"
)


def load_workflow():
    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def queue_prompt(workflow, client_id="hermes"):
    data = json.dumps({"prompt": workflow, "client_id": client_id}).encode("utf-8")
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_history(prompt_id):
    with urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}", timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_image(filename, subfolder="", folder_type="output"):
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
    url = f"{COMFY_URL}/view?{params}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="ref_premium_box.jpg", help="Input image filename in ComfyUI/input")
    parser.add_argument("--seed", type=int, default=random.randint(0, 2**32 - 1))
    parser.add_argument("--denoise", type=float, default=0.65)
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--negative", default=NEGATIVE)
    args = parser.parse_args()

    workflow = load_workflow()
    workflow["300"]["inputs"]["image"] = args.image
    workflow["238:227"]["inputs"]["text"] = args.prompt
    workflow["238:228"]["inputs"]["text"] = args.negative
    workflow["238:230"]["inputs"]["seed"] = args.seed
    workflow["238:230"]["inputs"]["denoise"] = args.denoise

    print(f"Queueing Qwen img2img (denoise={args.denoise}, seed={args.seed})...")
    result = queue_prompt(workflow)
    prompt_id = result["prompt_id"]
    print(f"Prompt ID: {prompt_id}")

    print("Waiting for completion...")
    while True:
        time.sleep(2)
        history = get_history(prompt_id)
        if prompt_id not in history:
            continue
        item = history[prompt_id]
        if item.get("status", {}).get("status_str") == "error":
            print("Generation failed:", item["status"].get("messages", []), file=sys.stderr)
            sys.exit(1)
        outputs = item.get("outputs", {})
        if outputs:
            break

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    saved = []
    for node_id, node_output in outputs.items():
        for img in node_output.get("images", []):
            data = fetch_image(img["filename"], img.get("subfolder", ""), img.get("type", "output"))
            out_path = os.path.join(OUTPUT_DIR, img["filename"])
            with open(out_path, "wb") as f:
                f.write(data)
            saved.append(out_path)
            print(f"Saved: {out_path}")

    if not saved:
        print("No images returned.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
