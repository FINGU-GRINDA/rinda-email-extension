#!/usr/bin/env python3
"""
Simple script to create placeholder icons for RINDA Email extension
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with RINDA branding"""
    # Create image with blue background
    img = Image.new('RGB', (size, size), color='#1a73e8')
    draw = ImageDraw.Draw(img)

    # Draw white circle in center
    circle_size = int(size * 0.7)
    circle_pos = (size - circle_size) // 2
    draw.ellipse(
        [circle_pos, circle_pos, circle_pos + circle_size, circle_pos + circle_size],
        fill='white'
    )

    # Draw "R" letter in blue
    try:
        # Try to use a nice font
        font_size = int(size * 0.5)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw "R" in center
    text = "R"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - bbox[1]

    draw.text((text_x, text_y), text, fill='#1a73e8', font=font)

    # Add small email icon indicator
    if size >= 48:
        # Draw small envelope in bottom right
        env_size = size // 4
        env_x = size - env_size - 4
        env_y = size - env_size - 4

        # Envelope rectangle
        draw.rectangle(
            [env_x, env_y, env_x + env_size, env_y + env_size],
            fill='#d93025',
            outline='white',
            width=1
        )

        # Envelope flap
        draw.line(
            [(env_x, env_y), (env_x + env_size//2, env_y + env_size//2)],
            fill='white',
            width=1
        )
        draw.line(
            [(env_x + env_size, env_y), (env_x + env_size//2, env_y + env_size//2)],
            fill='white',
            width=1
        )

    # Save image
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    """Create all required icon sizes"""
    icons_dir = 'icons'

    # Create icons directory if it doesn't exist
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)

    # Create icons in different sizes
    sizes = [
        (16, 'icon16.png'),
        (48, 'icon48.png'),
        (128, 'icon128.png')
    ]

    for size, filename in sizes:
        filepath = os.path.join(icons_dir, filename)
        create_icon(size, filepath)

    print("\n✅ All icons created successfully!")
    print("Icons saved in:", os.path.abspath(icons_dir))

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ PIL/Pillow not installed.")
        print("Install with: pip install Pillow")
        print("\nAlternatively, create icons manually:")
        print("1. Create 3 PNG images (16x16, 48x48, 128x128)")
        print("2. Save them as icon16.png, icon48.png, icon128.png in icons/ folder")
