#!/usr/bin/env python3
"""Generate an image with Qwen-Image 2512 (turbo LoRA) via local ComfyUI."""
import argparse
import json
import time
from pathlib import Path

import requests

HOST = "http://127.0.0.1:8188"
WORKFLOW = Path(__file__).resolve().parents[1] / "assets" / "workflows" / "qwen_image_2512_turbo.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "comfy_outputs"


def run_workflow(prompt: str, negative_prompt: str, width: int, height: int, seed: int, steps: int, cfg: float):
    workflow = json.loads(WORKFLOW.read_text())
    workflow["238:227"]["inputs"]["text"] = prompt
    workflow["238:228"]["inputs"]["text"] = negative_prompt
    workflow["238:232"]["inputs"]["width"] = width
    workflow["238:232"]["inputs"]["height"] = height
    workflow["238:230"]["inputs"]["seed"] = seed
    workflow["238:230"]["inputs"]["steps"] = steps
    workflow["238:230"]["inputs"]["cfg"] = cfg

    payload = {"prompt": workflow, "client_id": "fabia-qwen-2512"}
    resp = requests.post(f"{HOST}/prompt", json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"ComfyUI submit failed: {resp.status_code} {resp.text[:500]}")
    data = resp.json()
    prompt_id = data["prompt_id"]
    print(f"Submitted prompt_id={prompt_id}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for _ in range(600):  # 20 minutes max for big model
        time.sleep(2)
        hist = requests.get(f"{HOST}/history/{prompt_id}", timeout=60).json()
        if prompt_id in hist:
            outputs = hist[prompt_id].get("outputs", {})
            for node_id, node_out in outputs.items():
                for img in node_out.get("images", []):
                    filename = img["filename"]
                    subfolder = img.get("subfolder", "")
                    url = f"{HOST}/view?filename={filename}&subfolder={subfolder}&type=output"
                    img_data = requests.get(url, timeout=60).content
                    out_path = OUT_DIR / filename
                    out_path.write_bytes(img_data)
                    print(f"Saved: {out_path}")
                    return out_path
            raise RuntimeError("No image output found")
    raise RuntimeError("Timeout waiting for ComfyUI")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative", default="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感，构图混乱，文字模糊，扭曲")
    parser.add_argument("--width", type=int, default=1328)
    parser.add_argument("--height", type=int, default=1328)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--cfg", type=float, default=1.0)
    args = parser.parse_args()

    run_workflow(args.prompt, args.negative, args.width, args.height, args.seed, args.steps, args.cfg)


if __name__ == "__main__":
    main()
