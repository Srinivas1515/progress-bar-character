#!/usr/bin/env python3
"""Measure storyboard panels or video frames for progress-bar-character.

For each panel it reports: background purity, how far the border colour is from the locked
background colour, the mascot's bounding box, its height as % of the panel, its centre x as % of the
panel width, and where its feet sit. Compare against the shot plan (planner output).

Usage:
  python scripts/check_frame.py storyboard.png --bg green --grid 1x4 --expect-height 27 --expect-x 0,14,28,42
  python scripts/check_frame.py frame.png --bg black
  ffmpeg -ss 12 -i clip.mp4 -frames:v 1 frame.png   # grab a frame from a generated clip first

--bg: green | black | white | #RRGGBB     --grid: COLSxROWS (equal cells, row-major)
--trim: % of each cell to ignore at its edges (panel dividers, captions)     --tol: colour distance counted as background
"""
import argparse, sys
import numpy as np
from PIL import Image

NAMED = {"green": (0, 255, 0), "black": (0, 0, 0), "white": (255, 255, 255)}


def parse_bg(v):
    if v.lower() in NAMED:
        return NAMED[v.lower()]
    v = v.lstrip("#")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def analyse(cell, bg, tol, trim):
    H, W, _ = cell.shape                      # full panel: all percentages are relative to this
    ty, tx = int(H * trim / 100), int(W * trim / 100)
    c = cell[ty:H - ty, tx:W - tx].astype(float)
    dist = np.sqrt(((c - np.array(bg)) ** 2).sum(axis=2))
    fg = dist > tol
    purity = 100 * (1 - fg.mean())
    border = np.concatenate([c[0], c[-1], c[:, 0], c[:, -1]]).mean(axis=0)
    border_dev = float(np.sqrt(((border - np.array(bg)) ** 2).sum()))
    ys, xs = np.where(fg)
    res = {"purity_pct": round(purity, 2), "border_colour": [int(v) for v in border], "border_deviation": round(border_dev, 1)}
    if len(xs) < 30:
        res["mascot"] = None
        return res
    y0, y1 = np.percentile(ys, [0.3, 99.7]); x0, x1 = np.percentile(xs, [0.3, 99.7])
    X0, X1, Y0, Y1 = float(x0 + tx), float(x1 + tx), float(y0 + ty), float(y1 + ty)
    res["mascot"] = {"bbox": [int(X0), int(Y0), int(X1), int(Y1)],
                     "height_pct": round(100 * (Y1 - Y0) / H, 1),
                     "centre_x_pct": round(100 * ((X0 + X1) / 2) / W, 1),
                     "feet_y_pct": round(100 * Y1 / H, 1)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--bg", required=True)
    ap.add_argument("--grid", default="1x1")
    ap.add_argument("--tol", type=float, default=60)
    ap.add_argument("--trim", type=float, default=2.0)
    ap.add_argument("--expect-height", type=float, help="expected mascot height, %% of panel height")
    ap.add_argument("--expect-x", help="comma list of expected centre x %% per panel")
    a = ap.parse_args()

    bg = parse_bg(a.bg)
    img = np.array(Image.open(a.image).convert("RGB"))
    cols, rows = (int(v) for v in a.grid.lower().split("x"))
    H, W, _ = img.shape
    ch, cw = H // rows, W // cols
    ex = [float(v) for v in a.expect_x.split(",")] if a.expect_x else []
    flags_total = 0
    n = 0
    for r in range(rows):
        for c in range(cols):
            n += 1
            cell = img[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw]
            res = analyse(cell, bg, a.tol, a.trim)
            flags = []
            if res["purity_pct"] < 96: flags.append("background not flat (gradient, floor, shadow or props)")
            if res["border_deviation"] > 25: flags.append("background colour is off the locked colour")
            m = res["mascot"]
            if m is None: flags.append("no mascot found")
            else:
                if a.expect_height and abs(m["height_pct"] - a.expect_height) > 0.25 * a.expect_height:
                    flags.append(f"height {m['height_pct']}% vs expected {a.expect_height}% (more than 25% off; flying poses are taller, crouches shorter)")
                if ex and n <= len(ex) and abs(m["centre_x_pct"] - ex[n - 1]) > 4:
                    flags.append(f"x {m['centre_x_pct']}% vs expected {ex[n-1]}% (more than 4% off)")
            flags_total += len(flags)
            print(f"Panel {n}: purity {res['purity_pct']}% | border {res['border_colour']} (dev {res['border_deviation']}) | mascot {m}")
            for f in flags: print("   FLAG:", f)
    print(f"\n{n} panel(s) checked, {flags_total} flag(s).")
    sys.exit(0)


if __name__ == "__main__":
    main()
