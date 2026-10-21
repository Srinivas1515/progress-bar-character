#!/usr/bin/env python3
"""Check generated mascot clips against the moving-ground rule.

1) SPEED mode - is the mascot carried at a constant speed with no stalls?
   python scripts/track_motion.py clip.mp4 --bg black --expect-speed 1.766 --role first
   (role: first = must be entering at 0.0 s | middle = fully inside at both ends | last = must be leaving at the end | single = both)

2) JOINT mode - does clip B start exactly where clip A ended?
   python scripts/track_motion.py --joint clipA.mp4 clipB.mp4 --bg black

Needs ffmpeg/ffprobe. --bg: green | black | white | #RRGGBB. Positions are % of frame width, speed is %/s.
Take --expect-speed from scripts/plan_shots.py ("carry_speed_pct_per_s").
"""
import argparse, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

NAMED = {"green": (0, 255, 0), "black": (0, 0, 0), "white": (255, 255, 255)}


def parse_bg(v):
    if v.lower() in NAMED: return NAMED[v.lower()]
    v = v.lstrip("#"); return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height:format=duration", "-of", "csv=p=0", path]).decode().split()
    wh = out[0].split(","); return int(wh[0]), int(wh[1]), float(out[1]) if len(out) > 1 else None


def measure(img, bg, tol):
    """img: HxWx3 uint8. Returns dict of mascot edges in % of frame, or None."""
    H, W, _ = img.shape
    d = np.sqrt(((img.astype(float) - np.array(bg)) ** 2).sum(axis=2))
    ys, xs = np.where(d > tol)
    if len(xs) < 20: return None
    x0, x1 = np.percentile(xs, [0.3, 99.7]); y0, y1 = np.percentile(ys, [0.3, 99.7])
    return {"left": 100 * x0 / W, "right": 100 * x1 / W, "centre": 100 * (x0 + x1) / 2 / W,
            "height": 100 * (y1 - y0) / H, "feet": 100 * y1 / H, "top": 100 * y0 / H}


def frames(path, fps, width=640):
    w, h, dur = probe(path)
    sh = int(round(h * width / w / 2) * 2)
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={width}:{sh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = width * sh * 3; i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield i / fps, np.frombuffer(b, np.uint8).reshape(sh, width, 3); i += 1


def speed_mode(a, bg):
    rows = [(t, measure(f, bg, a.tol)) for t, f in frames(a.clip, a.fps)]
    if not rows: sys.exit("No frames read.")
    print(f"{len(rows)} samples at {a.fps} per second")
    valid = [(t, m["centre"]) for t, m in rows if m and m["left"] > 1.5 and m["right"] < 98.5]
    flags = []
    first, last = rows[0][1], rows[-1][1]
    if a.role in ("first", "single"):
        if first is None: flags.append("role first: no mascot visible at 0.0 s (front edge should already be inside the left edge)")
        elif first["left"] > 3 and first["right"] > 8: flags.append(f"role first: mascot is already well inside the frame at 0.0 s (left edge {first['left']:.1f}%)")
    if a.role in ("last", "single"):
        if last is not None and last["left"] < 90: flags.append(f"role last: mascot still clearly in frame on the last sample (left edge {last['left']:.1f}%)")
    if a.role == "middle":
        for nm, m in (("start", first), ("end", last)):
            if m is None or m["left"] < 1.5 or m["right"] > 98.5: flags.append(f"role middle: mascot is not fully inside the frame at the {nm}")
    if len(valid) >= 4:
        t = np.array([v[0] for v in valid]); x = np.array([v[1] for v in valid])
        slope, icpt = np.polyfit(t, x, 1); fit = slope * t + icpt
        ss_res = ((x - fit) ** 2).sum(); ss_tot = ((x - x.mean()) ** 2).sum() or 1e-9
        r2 = 1 - ss_res / ss_tot; maxdev = np.abs(x - fit).max()
        print(f"Fully-inside samples: {len(valid)} | fitted speed {slope:.3f} %/s | R^2 {r2:.4f} | max deviation from a straight line {maxdev:.2f}% of width")
        exp = a.expect_speed or slope
        dt = 1.0 / a.fps; stall = 0; worst = 0
        for k in range(1, len(valid)):
            step = valid[k][1] - valid[k - 1][1]
            if step < 0.35 * exp * (valid[k][0] - valid[k - 1][0]): stall += 1; worst = max(worst, stall)
            else: stall = 0
        if a.expect_speed and abs(slope - a.expect_speed) > 0.15 * a.expect_speed:
            flags.append(f"speed {slope:.3f} %/s is more than 15% off the planned {a.expect_speed} %/s")
        if maxdev > 1.5: flags.append(f"position wobbles up to {maxdev:.2f}% of the width around a straight line (speed is not constant)")
        if worst * dt >= 0.75: flags.append(f"mascot stalls for about {worst*dt:.1f}s (progress under 35% of the planned speed)")
        if slope <= 0: flags.append("mascot is not moving to the right")
    else:
        print("Too few fully-inside samples to fit a speed (clip may be mostly entering or leaving).")
    for t, m in rows[:: max(1, int(a.fps * 2))]:
        print(f"  t={t:5.1f}s  " + ("no mascot" if m is None else f"left {m['left']:5.1f}%  right {m['right']:5.1f}%  centre {m['centre']:5.1f}%  height {m['height']:4.1f}%  feet {m['feet']:4.1f}%"))
    report(flags)


def grab(path, which, tmp):
    out = os.path.join(tmp, f"{which}_{os.path.basename(path)}.png")
    if which == "first":
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", path, "-frames:v", "1", out])
    else:
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", path, "-update", "1", out])
    return np.array(Image.open(out).convert("RGB"))


def joint_mode(a, bg):
    with tempfile.TemporaryDirectory() as tmp:
        fa, fb = grab(a.joint[0], "last", tmp), grab(a.joint[1], "first", tmp)
    if fa.shape != fb.shape:
        fb = np.array(Image.fromarray(fb).resize((fa.shape[1], fa.shape[0])))
    ma, mb = measure(fa, bg, a.tol), measure(fb, bg, a.tol)
    flags = []
    print("Last frame of A :", None if ma is None else {k: round(float(v), 1) for k, v in ma.items()})
    print("First frame of B:", None if mb is None else {k: round(float(v), 1) for k, v in mb.items()})
    if ma is None or mb is None:
        flags.append("no mascot found in one of the two frames")
    else:
        dx = abs(ma["centre"] - mb["centre"]); dh = abs(ma["height"] - mb["height"]) / max(ma["height"], 1) * 100; df = abs(ma["feet"] - mb["feet"])
        print(f"Difference: centre x {dx:.2f}% of width | height {dh:.1f}% | feet {df:.2f}% of frame height")
        if dx > 1.5: flags.append(f"x differs by {dx:.2f}% of the width (should be under 1.5%)")
        if dh > 10: flags.append(f"mascot size differs by {dh:.0f}% between the two frames")
        if df > 2: flags.append(f"feet height differs by {df:.1f}% of the frame height")
        x0 = int(min(ma["left"], mb["left"]) / 100 * fa.shape[1]); x1 = int(max(ma["right"], mb["right"]) / 100 * fa.shape[1]) + 1
        diff = np.abs(fa[:, x0:x1].astype(int) - fb[:, x0:x1].astype(int)).mean()
        print(f"Mean pixel difference around the mascot: {diff:.1f} / 255 (pose, face or cape differences raise it)")
        if diff > 25: flags.append("the two frames look different (pose, expression or cape state may not match)")
    report(flags)


def report(flags):
    print()
    if not flags: print("OK: no flags.")
    for f in flags: print("FLAG:", f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", nargs="?")
    ap.add_argument("--joint", nargs=2, metavar=("CLIP_A", "CLIP_B"))
    ap.add_argument("--bg", required=True)
    ap.add_argument("--fps", type=float, default=2.0, help="samples per second in speed mode")
    ap.add_argument("--tol", type=float, default=60)
    ap.add_argument("--expect-speed", type=float, help="planned carry speed in %% of frame width per second")
    ap.add_argument("--role", default="middle", choices=["first", "middle", "last", "single"])
    a = ap.parse_args(); bg = parse_bg(a.bg)
    if a.joint: joint_mode(a, bg)
    elif a.clip: speed_mode(a, bg)
    else: ap.error("give a clip, or --joint A B")


if __name__ == "__main__":
    main()
