"""Generate Android launcher icons for Restoran admin app."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android" / "app" / "src" / "main" / "res"
IOS_ICON = (
    ROOT / "ios" / "App" / "App" / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon-512@2x.png"
)
BRAND = (255, 90, 31)
BRAND_LIGHT = (255, 138, 76)
WHITE = (255, 255, 255, 255)

SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

FOREGROUND_SIZES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient_background(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    radius = round(size * 0.22)
    for y in range(size):
        t = y / max(size - 1, 1)
        r = lerp(BRAND[0], BRAND_LIGHT[0], t)
        g = lerp(BRAND[1], BRAND_LIGHT[1], t)
        b = lerp(BRAND[2], BRAND_LIGHT[2], t)
        for x in range(size):
            if _inside_rounded_rect(x, y, size, size, radius):
                px[x, y] = (r, g, b, 255)
    return img


def _inside_rounded_rect(x: int, y: int, w: int, h: int, r: int) -> bool:
    if x < r and y < r:
        return (x - r) ** 2 + (y - r) ** 2 <= r**2
    if x >= w - r and y < r:
        return (x - (w - r - 1)) ** 2 + (y - r) ** 2 <= r**2
    if x < r and y >= h - r:
        return (x - r) ** 2 + (y - (h - r - 1)) ** 2 <= r**2
    if x >= w - r and y >= h - r:
        return (x - (w - r - 1)) ** 2 + (y - (h - r - 1)) ** 2 <= r**2
    return True


def draw_symbol(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
  x0, y0, x1, y1 = box
  w = x1 - x0
  h = y1 - y0
  cx = (x0 + x1) / 2
  cy = (y0 + y1) / 2

  fork_x = cx - w * 0.14
  prong_w = max(2, int(w * 0.045))
  prong_h = max(6, int(h * 0.22))
  gap = max(2, int(w * 0.03))
  handle_w = max(3, int(w * 0.07))
  handle_h = max(8, int(h * 0.28))
  top = cy - h * 0.18
  for i, dx in enumerate([-gap - prong_w, 0, gap + prong_w]):
    draw.rounded_rectangle(
      (fork_x + dx - prong_w / 2, top, fork_x + dx + prong_w / 2, top + prong_h),
      radius=max(1, prong_w // 3),
      fill=WHITE,
    )
  draw.rounded_rectangle(
    (fork_x - handle_w / 2, top + prong_h * 0.55, fork_x + handle_w / 2, top + prong_h + handle_h),
    radius=max(2, handle_w // 3),
    fill=WHITE,
  )

  knife_x = cx + w * 0.16
  blade_w = max(4, int(w * 0.08))
  blade_h = max(10, int(h * 0.34))
  draw.pieslice(
    (knife_x - blade_w / 2, top - blade_h * 0.08, knife_x + blade_w / 2, top + blade_h),
    start=200,
    end=340,
    fill=WHITE,
  )
  draw.rounded_rectangle(
    (knife_x - blade_w * 0.35, top + blade_h * 0.55, knife_x + blade_w * 0.35, top + blade_h + handle_h * 0.85),
    radius=max(2, blade_w // 3),
    fill=WHITE,
  )

  shadow_w = int(w * 0.42)
  shadow_h = max(3, int(h * 0.05))
  draw.ellipse(
    (cx - shadow_w / 2, y1 - h * 0.12, cx + shadow_w / 2, y1 - h * 0.12 + shadow_h * 2),
    fill=(255, 255, 255, 70),
  )


def draw_qr_hint(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
  x0, y0, x1, y1 = box
  size = min(x1 - x0, y1 - y0)
  cell = max(2, int(size * 0.11))
  gx = x1 - cell * 4.2
  gy = y1 - cell * 4.2
  pattern = [
    "1110011",
    "1010010",
    "1110011",
    "0001010",
    "1101101",
    "1010001",
    "1110111",
  ]
  for row, bits in enumerate(pattern):
    for col, bit in enumerate(bits):
      if bit == "1":
        draw.rectangle(
          (gx + col * cell, gy + row * cell, gx + (col + 1) * cell - 1, gy + (row + 1) * cell - 1),
          fill=(255, 255, 255, 220),
        )


def compose_icon(size: int, safe_scale: float = 0.62) -> Image.Image:
  base = gradient_background(size)
  draw = ImageDraw.Draw(base)
  pad = size * (1 - safe_scale) / 2
  symbol_box = (pad, pad, size - pad, size - pad)
  draw_symbol(draw, symbol_box)
  draw_qr_hint(draw, symbol_box)
  return base


def compose_foreground(size: int) -> Image.Image:
  img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)
  pad = size * 0.18
  box = (pad, pad, size - pad, size - pad)
  draw_symbol(draw, box)
  draw_qr_hint(draw, box)
  return img


def main() -> None:
  for folder, size in SIZES.items():
    target = RES / folder
    target.mkdir(parents=True, exist_ok=True)
    icon = compose_icon(size)
    icon.save(target / "ic_launcher.png")
    icon.save(target / "ic_launcher_round.png")

  for folder, size in FOREGROUND_SIZES.items():
    target = RES / folder
    target.mkdir(parents=True, exist_ok=True)
    compose_foreground(size).save(target / "ic_launcher_foreground.png")

  IOS_ICON.parent.mkdir(parents=True, exist_ok=True)
  compose_icon(1024).save(IOS_ICON)
  print("iOS icon generated at", IOS_ICON)

  print("Icons generated in", RES)


if __name__ == "__main__":
  main()
