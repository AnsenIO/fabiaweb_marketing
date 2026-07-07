#!/usr/bin/env python3
"""Add a small circular 'F' logo onto the mini PC front panel."""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def add_f_logo(input_path: str, output_path: str,
               box_norm=(0.67, 0.63, 0.71, 0.67),
               bg_color=(30, 30, 35), border_color=(180, 150, 100),
               text_color=(240, 240, 245)):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    x1 = int(box_norm[0] * width)
    y1 = int(box_norm[1] * height)
    x2 = int(box_norm[2] * width)
    y2 = int(box_norm[3] * height)

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    radius = min(x2 - x1, y2 - y1) // 2

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Outer metallic ring
    draw.ellipse([cx - radius - 2, cy - radius - 2, cx + radius + 2, cy + radius + 2],
                 fill=border_color + (255,))
    # Inner dark circle
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=bg_color + (255,))

    # Letter F
    font_dir = "/usr/share/fonts/truetype/dejavu"
    font_size = int(radius * 1.2)
    font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), font_size)
    text = "F"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = cy - th // 2 - bbox[1]
    draw.text((tx, ty), text, font=font, fill=text_color + (255,),
              stroke_width=max(1, radius // 12), stroke_fill=(0, 0, 0, 120))

    img = Image.alpha_composite(img, overlay)
    img.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="output.png")
    parser.add_argument("--box", default="0.67,0.63,0.71,0.67")
    args = parser.parse_args()
    box = tuple(float(v) for v in args.box.split(","))
    add_f_logo(args.input, args.output, box)


if __name__ == "__main__":
    main()
