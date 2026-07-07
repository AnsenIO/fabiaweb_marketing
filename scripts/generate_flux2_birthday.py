#!/usr/bin/env python3
"""Generate a FABIABox birthday image using Flux 2 via ComfyUI API."""
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
WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "workflows", "flux2_text_to_image.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "comfy_outputs")

PROMPT = (
    "Premium cinematic product photography of a compact dark gunmetal and copper mini PC workstation, "
    "with dense vertical heatsink fins glowing warm amber from within, sitting on a polished wooden desk "
    "inside a luxurious high-tech penthouse office at night. Floor-to-ceiling windows show a softly blurred "
    "city skyline bokeh. Holographic blue data visualizations float in the background. Navy and electric "
    "orange confetti falling gently. A single lit birthday candle sits on top of the heatsink, warm flame "
    "reflecting on metal. Dramatic low-key cinematic lighting, photorealistic, 8K, shallow depth of field. "
    "No text, no logos, no branding, no typography, no words."
)


def load_workflow():
    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        wf = json.load(f)
    # Convert UI-format single links [[node_id, slot]] -> [node_id, slot]
    for node_id, node in wf.items():
        inputs = node.get("inputs", {})
        for key, value in list(inputs.items()):
            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], list) and len(value[0]) == 2:
                first, second = value[0]
                if isinstance(first, (str, int)) and isinstance(second, int):
                    inputs[key] = [first, second]
    return wf


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
    parser.add_argument("--seed", type=int, default=random.randint(0, 2**32 - 1))
    parser.add_argument("--width", type=int, default=1344)
    parser.add_argument("--height", type=int, default=1344)
    parser.add_argument("--prompt", default=PROMPT)
    args = parser.parse_args()

    workflow = load_workflow()
    workflow["6"]["inputs"]["text"] = args.prompt
    workflow["25"]["inputs"]["noise_seed"] = args.seed
    workflow["47"]["inputs"]["width"] = args.width
    workflow["47"]["inputs"]["height"] = args.height
    workflow["48"]["inputs"]["width"] = args.width
    workflow["48"]["inputs"]["height"] = args.height

    print(f"Queueing Flux 2 birthday generation ({args.width}x{args.height}) with seed {args.seed}...")
    result = queue_prompt(workflow)
    prompt_id = result["prompt_id"]
    print(f"Prompt ID: {prompt_id}")

    print("Waiting for completion...")
    while True:
        time.sleep(3)
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
