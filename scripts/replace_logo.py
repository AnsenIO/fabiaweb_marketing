#!/usr/bin/env python3
"""Replace the logo on the mini PC front panel with custom text."""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def replace_logo(input_path: str, output_path: str, text: str = "F.A.B.I.A.",
                 box_norm=(0.54, 0.61, 0.65, 0.65), text_color=(220, 230, 255, 255),
                 bg_color=(35, 35, 38, 230)):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    x1 = int(box_norm[0] * width)
    y1 = int(box_norm[1] * height)
    x2 = int(box_norm[2] * width)
    y2 = int(box_norm[3] * height)

    draw = ImageDraw.Draw(img)
    # Rounded rectangle to cover existing logo
    draw.rounded_rectangle([x1, y1, x2, y2], radius=4, fill=bg_color)

    font_dir = "/usr/share/fonts/truetype/dejavu"
    font = None
    for font_size in range(26, 10, -2):
        font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        if text_w < (x2 - x1) * 0.9 and text_h < (y2 - y1) * 0.8:
            break
    if font is None:
        font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), 12)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_h = bbox[3] - bbox[1]

    # Draw each character with a little spacing to mimic a technical logo
    total_w = 0
    char_bboxes = []
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        cw = bbox[2] - bbox[0]
        char_bboxes.append(cw)
        total_w += cw
    spacing = max(1, int((x2 - x1 - total_w) / (len(text) + 1)))
    start_x = x1 + spacing
    cy = y1 + ((y2 - y1) - text_h) // 2 - bbox[1]
    x = start_x
    for i, ch in enumerate(text):
        draw.text((x, cy), ch, font=font, fill=text_color)
        x += char_bboxes[i] + spacing

    img.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="output.png")
    parser.add_argument("--text", default="F.A.B.I.A.")
    parser.add_argument("--box", default="0.54,0.61,0.65,0.65")
    args = parser.parse_args()
    box = tuple(float(v) for v in args.box.split(","))
    replace_logo(args.input, args.output, args.text, box)


if __name__ == "__main__":
    main()
