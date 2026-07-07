#!/usr/bin/env python3
"""Add a vertical F.A.B.I.A. logo along the front-right edge of the mini PC."""
import argparse
import math
import os
from PIL import Image, ImageDraw, ImageFont


def add_vertical_logo(input_path: str, output_path: str, text: str = "F.A.B.I.A.",
                      top_norm=(0.865, 0.512), bottom_norm=(0.865, 0.748),
                      offset_ratio=-0.015, font_color=(220, 230, 255)):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    x_top = top_norm[0] * width
    y_top = top_norm[1] * height
    x_bot = bottom_norm[0] * width
    y_bot = bottom_norm[1] * height

    dx = x_bot - x_top
    dy = y_bot - y_top
    edge_len = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dx, dy))  # angle from vertical; negative if leaning right

    # Create transparent strip tall enough for stacked characters
    font_dir = "/usr/share/fonts/truetype/dejavu"
    font_size = int(edge_len / (len(text) * 1.15))
    font = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), font_size)

    # Measure max char size
    max_w = 0
    total_h = 0
    char_dims = []
    draw_tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    for ch in text:
        bbox = draw_tmp.textbbox((0, 0), ch, font=font)
        cw, ch_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        char_dims.append((cw, ch_h))
        max_w = max(max_w, cw)
        total_h += ch_h
    spacing = int((edge_len - total_h) / (len(text) + 1))
    strip_h = edge_len
    strip_w = max_w + 10

    strip = Image.new("RGBA", (strip_w, int(strip_h)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(strip)
    y = spacing
    for i, ch in enumerate(text):
        cw, ch_h = char_dims[i]
        x = (strip_w - cw) // 2
        draw.text((x, y), ch, font=font, fill=font_color + (255,), stroke_width=1, stroke_fill=(20, 20, 25, 180))
        y += ch_h + spacing

    # Rotate strip to match edge angle
    rotated = strip.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)

    # Compute paste position: center of rotated strip should lie along the edge, offset left
    # Midpoint of edge
    mid_x = (x_top + x_bot) / 2
    mid_y = (y_top + y_bot) / 2
    # Offset perpendicular to edge (toward viewer / front face)
    perp_x = -dy / edge_len
    perp_y = dx / edge_len
    off_x = mid_x + perp_x * offset_ratio * width
    off_y = mid_y + perp_y * offset_ratio * width

    paste_x = int(off_x - rotated.width / 2)
    paste_y = int(off_y - rotated.height / 2)

    img.paste(rotated, (paste_x, paste_y), rotated)
    img.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="output.png")
    parser.add_argument("--text", default="F.A.B.I.A.")
    parser.add_argument("--top", default="0.865,0.512")
    parser.add_argument("--bottom", default="0.865,0.748")
    parser.add_argument("--offset", type=float, default=-0.015)
    args = parser.parse_args()
    top = tuple(float(v) for v in args.top.split(","))
    bottom = tuple(float(v) for v in args.bottom.split(","))
    add_vertical_logo(args.input, args.output, args.text, top, bottom, args.offset)


if __name__ == "__main__":
    main()
