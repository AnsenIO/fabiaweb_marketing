#!/usr/bin/env python3
"""Overlay FABIABox birthday text onto an image using PIL."""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def overlay_text(input_path: str, output_path: str, headline: str = "Happy Birthday FABIABox",
                 tagline: str = "The AI Co-Founder That Ships Your Company.", url: str = "shop.fabiabox.com"):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size

    # Dark gradient bar at the bottom
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    bar_height = int(height * 0.16)
    for i in range(bar_height):
        alpha = int(180 * (i / bar_height))
        draw.line([(0, height - bar_height + i), (width, height - bar_height + i)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    font_dir = "/usr/share/fonts/truetype/dejavu"
    font_large = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), int(height * 0.055))
    font_medium = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans.ttf"), int(height * 0.028))
    font_small = ImageFont.truetype(os.path.join(font_dir, "DejaVuSans-Bold.ttf"), int(height * 0.024))

    # Main headline
    bbox = draw.textbbox((0, 0), headline, font=font_large)
    text_w = bbox[2] - bbox[0]
    y = height - bar_height + int(bar_height * 0.18)
    draw.text(((width - text_w) / 2, y), headline, font=font_large, fill=(255, 255, 255, 255))

    # Tagline
    bbox = draw.textbbox((0, 0), tagline, font=font_medium)
    text_w = bbox[2] - bbox[0]
    y += int(height * 0.06)
    draw.text(((width - text_w) / 2, y), tagline, font=font_medium, fill=(200, 220, 255, 255))

    # URL
    bbox = draw.textbbox((0, 0), url, font=font_small)
    text_w = bbox[2] - bbox[0]
    y += int(height * 0.05)
    draw.text(((width - text_w) / 2, y), url, font=font_small, fill=(255, 140, 0, 255))

    img.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input image path")
    parser.add_argument("--output", default="output.png", help="Output image path")
    parser.add_argument("--headline", default="Happy Birthday FABIABox")
    parser.add_argument("--tagline", default="The AI Co-Founder That Ships Your Company.")
    parser.add_argument("--url", default="shop.fabiabox.com")
    args = parser.parse_args()
    overlay_text(args.input, args.output, args.headline, args.tagline, args.url)


if __name__ == "__main__":
    main()
