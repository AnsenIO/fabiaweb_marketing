#!/usr/bin/env python3
"""Generate a FABIABox birthday social-media graphic via local ComfyUI."""
import argparse
import json
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

HOST = "http://127.0.0.1:8188"
WORKFLOW = Path(__file__).resolve().parents[1] / "assets" / "workflows" / "flux_fp8_birthday.json"
OUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "social"


def overlay_text(src_path: Path, dst_path: Path):
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        cta_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()

    bar_h = 220
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    title = "Happy Birthday FABIABox"
    sub = "The AI Co-Founder That Ships Your Company"
    cta = "fabiabox.com"

    y_start = h - bar_h + 30
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((w - (bbox[2] - bbox[0])) // 2, y_start), title, font=title_font, fill=(255, 255, 255))

    bbox = draw.textbbox((0, 0), sub, font=sub_font)
    draw.text(((w - (bbox[2] - bbox[0])) // 2, y_start + 85), sub, font=sub_font, fill=(230, 230, 230))

    bbox = draw.textbbox((0, 0), cta, font=cta_font)
    draw.text(((w - (bbox[2] - bbox[0])) // 2, y_start + 140), cta, font=cta_font, fill=(255, 140, 0))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img.save(dst_path)
    print(f"Saved final graphic: {dst_path}")


def run_workflow(prompt: str, negative_prompt: str, seed: int, steps: int):
    workflow = json.loads(WORKFLOW.read_text())
    workflow.pop("_comment", None)
    workflow["6"]["inputs"]["text"] = prompt
    # Flux workflow doesn't have a negative prompt node by default; ignore if missing.
    if "7" in workflow:
        workflow["7"]["inputs"]["text"] = negative_prompt
    workflow["25"]["inputs"]["noise_seed"] = seed
    workflow["17"]["inputs"]["steps"] = steps

    payload = {"prompt": workflow, "client_id": "fabia-birthday"}
    resp = requests.post(f"{HOST}/prompt", json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"ComfyUI submit failed: {resp.status_code} {resp.text[:200]}")
    data = resp.json()
    prompt_id = data["prompt_id"]
    print(f"Submitted prompt_id={prompt_id}")

    for _ in range(180):  # 6 minutes
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
                    base_path = OUT_DIR / filename
                    base_path.write_bytes(img_data)
                    print(f"Downloaded base image: {base_path}")
                    return base_path
            raise RuntimeError("No image output found")
    raise RuntimeError("Timeout waiting for ComfyUI")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="A premium dark-themed social media graphic for a tech company called FABIABox. Center: a sleek matte-black AI appliance box with a subtle glowing candle on top, surrounded by elegant navy and electric-orange confetti. Clean, minimalist, celebratory, high-end startup aesthetic, square 1:1 composition, deep charcoal gradient background, soft studio lighting, ultra detailed, 8k")
    parser.add_argument("--negative", default="blurry, low quality, distorted text, watermark, signature, cluttered, cartoonish, cheap")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--output", default=str(OUT_DIR / "fabiabox_birthday_post.png"))
    args = parser.parse_args()

    base_path = run_workflow(args.prompt, args.negative, args.seed, args.steps)
    overlay_text(base_path, Path(args.output))


if __name__ == "__main__":
    main()
