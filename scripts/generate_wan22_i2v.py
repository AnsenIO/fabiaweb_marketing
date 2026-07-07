#!/usr/bin/env python3
"""Generate a 5-second image-to-video clip from a FABIABox image using Wan 2.2."""
import argparse
import json
import os
import random
import sys
import time
import urllib.request
import urllib.parse

COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "workflows", "wan22_image_to_video.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "comfy_outputs")

PROMPT = (
    "Cinematic slow dolly around a premium dark gunmetal and copper mini PC workstation, "
    "the FABIABox, with vertical heatsink fins glowing warm amber and a single lit birthday "
    "candle flickering on top. Subtle camera movement, gentle flame flicker, amber light "
    "pulsing softly inside the heatsink. Luxury high-tech penthouse office at night, city "
    "skyline bokeh through floor-to-ceiling windows, holographic blue data displays "
    "animating in the background. Vibrant saturated colors, photorealistic, 8K."
)
NEGATIVE = (
    "静态，模糊不清，字幕，风格，画作，静止，低质量，丑陋，残缺，变形，多余手指，"
    "画面抖动，过曝，黑屏，镜头快速移动，人物，文字"
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


def fetch_video(filename, subfolder="", folder_type="output"):
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": folder_type})
    url = f"{COMFY_URL}/view?{params}"
    with urllib.request.urlopen(url, timeout=120) as resp:
        return resp.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="fabiabox_birthday_qwen_v12.png")
    parser.add_argument("--seed", type=int, default=random.randint(0, 2**32 - 1))
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--negative", default=NEGATIVE)
    args = parser.parse_args()

    workflow = load_workflow()
    workflow["200"]["inputs"]["image"] = args.image
    workflow["89"]["inputs"]["text"] = args.prompt
    workflow["72"]["inputs"]["text"] = args.negative
    workflow["81"]["inputs"]["noise_seed"] = args.seed

    print(f"Queueing Wan 2.2 image-to-video (seed {args.seed})...")
    result = queue_prompt(workflow)
    prompt_id = result["prompt_id"]
    print(f"Prompt ID: {prompt_id}")

    print("Waiting for completion...")
    while True:
        time.sleep(10)
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
        for vid in node_output.get("gifs", []):
            data = fetch_video(vid["filename"], vid.get("subfolder", ""), vid.get("type", "output"))
            out_path = os.path.join(OUTPUT_DIR, vid["filename"])
            with open(out_path, "wb") as f:
                f.write(data)
            saved.append(out_path)
            print(f"Saved: {out_path}")

    if not saved:
        print("No videos returned.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
