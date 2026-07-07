#!/usr/bin/env python3
"""Replace the front-panel F logo with a reference image (e.g. user-supplied emblem)."""
import argparse
import os
from typing import Tuple

from PIL import Image, ImageFilter, ImageChops


def replace_logo(base_path: str, logo_path: str, output_path: str, box: Tuple[float, float, float, float]):
    base = Image.open(base_path).convert("RGBA")
    w, h = base.size
    x1, y1, x2, y2 = int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)
    target_w = x2 - x1
    target_h = y2 - y1

    logo = Image.open(logo_path).convert("RGBA")
    lw, lh = logo.size
    scale = min(target_w / lw, target_h / lh)
    new_size = (int(lw * scale), int(lh * scale))
    logo = logo.resize(new_size, Image.Resampling.LANCZOS)

    paste_x = x1 + (target_w - new_size[0]) // 2
    paste_y = y1 + (target_h - new_size[1]) // 2

    # Build a purple glow behind the logo using its alpha channel
    alpha = logo.split()[-1]
    glow_rgb = Image.merge("RGB", [alpha, alpha, alpha])
    purple = Image.new("RGB", glow_rgb.size, (180, 40, 255))
    glow_purple = ImageChops.multiply(glow_rgb, purple)
    glow_purple.putalpha(alpha)
    radius = max(target_w, target_h) // 4
    glow_blur = glow_purple.filter(ImageFilter.GaussianBlur(radius=radius))

    # Paste the blurred glow onto a transparent canvas at the right location
    glow_canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_canvas.paste(glow_blur, (paste_x, paste_y), glow_blur)

    logo_canvas = Image.new("RGBA", base.size, (0, 0, 0, 0))
    logo_canvas.paste(logo, (paste_x, paste_y), logo)

    base = Image.alpha_composite(base, glow_canvas)
    base = Image.alpha_composite(base, logo_canvas)

    base.convert("RGB").save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base")
    parser.add_argument("--logo", default="/tmp/logo_transparent.png")
    parser.add_argument("--output", required=True)
    parser.add_argument("--box", required=True, help="x1,y1,x2,y2 normalized")
    args = parser.parse_args()
    box = tuple(float(v) for v in args.box.split(","))
    replace_logo(args.base, args.logo, args.output, box)
