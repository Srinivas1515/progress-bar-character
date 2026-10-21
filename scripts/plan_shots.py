#!/usr/bin/env python3
"""Shot divider, constant-speed position map and mascot-size calculator for progress-bar-character.

THE MOVING-GROUND RULE
The mascot is carried to the right by an invisible moving ground at ONE constant speed for the whole run,
whatever it is doing (walking, waving, dancing, standing, flying). Like a treadmill in reverse: its feet stay
planted on the ground and the ground carries it right. So position is a straight line in time:
  - t = 0:   the front edge of the mascot is just inside the left edge of the frame (a sliver is visible).
  - t = end: the rear edge of the mascot has just left the right edge of the frame.
Positions below are the mascot's CENTRE as a % of frame width (negative = partly off the left edge,
above 100 = partly off the right edge).

Examples:
  python scripts/plan_shots.py --duration 60 --cap 30 --aspect 9:16
  python scripts/plan_shots.py --duration 45 --cap 10 --aspect 16:9 --gen-aspect 16:9 --mascot-aspect 0.7
  python scripts/plan_shots.py --duration 60 --cap 10 --aspect 9:16 --csv positions.csv --json

Size: the mascot clip is a full-width strip generated in --gen-aspect (21:9 default, 16:9 if the tool has no
ultra-wide), scaled to the video width and placed at the bottom. Final mascot height is --mascot-pct of the
VIDEO height (default 6.5% for 9:16, 12% for 16:9). The script converts it to the % of the GENERATED frame
height used in prompts and warns when it is too small to generate well.
"""
import argparse, csv, json, math

DEFAULT_PCT = {"9:16": 6.5, "16:9": 12.0}
WINDOW = {"9:16": (5.5, 8.0), "16:9": (10.0, 14.0)}
VIDEO_PX = {"9:16": (1080, 1920), "16:9": (1920, 1080)}


def divide(duration, cap, min_last=3.0):
    """Shots of the tool's max length plus a shorter last shot for the remainder.
    A remainder under min_last seconds is merged: the last two shots are split evenly."""
    n = math.ceil(duration / cap - 1e-9)
    lens = [cap] * (n - 1)
    last = duration - cap * (n - 1)
    if last < min_last and n > 1:
        total = cap + last
        lens[-1] = math.ceil(total / 2)
        lens.append(total - lens[-1])
    else:
        lens.append(last)
    out, t = [], 0.0
    for i, L in enumerate(lens, 1):
        out.append({"shot": i, "start": t, "end": t + L, "length": L})
        t += L
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, required=True, help="progress-bar run time in seconds")
    ap.add_argument("--cap", type=float, required=True, help="max seconds per generation for the tool")
    ap.add_argument("--aspect", default="9:16", choices=["9:16", "16:9"], help="aspect ratio of the main video")
    ap.add_argument("--video-width", type=int)
    ap.add_argument("--video-height", type=int)
    ap.add_argument("--gen-aspect", default="21:9", help="aspect ratio the mascot clips are generated in (21:9 or 16:9)")
    ap.add_argument("--mascot-pct", type=float, help="final mascot height as %% of video height")
    ap.add_argument("--mascot-aspect", type=float, default=0.6,
                    help="mascot bounding-box width / height, including signature item (cape, tail, wings). Default 0.6")
    ap.add_argument("--sliver-pct", type=float, default=1.0, help="how much of the front edge is inside the frame at t=0, %% of frame width")
    ap.add_argument("--ground-pct", type=float, default=88.0, help="ground line, %% of generated frame height from the top")
    ap.add_argument("--bottom-margin-pct", type=float, default=0.0, help="gap between strip bottom and video bottom, %% of video height")
    ap.add_argument("--step", type=float, default=5.0, help="seconds between rows of the printed position table")
    ap.add_argument("--csv", help="write the per-second position table to this CSV file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    vw, vh = VIDEO_PX[a.aspect]
    vw = a.video_width or vw
    vh = a.video_height or vh
    pct = a.mascot_pct if a.mascot_pct is not None else DEFAULT_PCT[a.aspect]
    T = a.duration

    mascot_h = vh * pct / 100
    mascot_w = mascot_h * a.mascot_aspect
    w_pct = mascot_w / vw * 100
    x0 = a.sliver_pct - w_pct / 2          # centre at t=0 (front edge = sliver_pct)
    x1 = 100 + w_pct / 2                   # centre at t=T (rear edge = 100)
    v = (x1 - x0) / T                      # % of frame width per second
    v_px = v * vw / 100
    heights_per_s = v_px / mascot_h

    def x_at(t): return x0 + v * t
    t_inside = (w_pct - a.sliver_pct) / v                  # rear edge crosses the left edge: fully in frame
    t_exit_start = (100 - (x0 + w_pct / 2)) / v            # front edge reaches the right edge

    shots = divide(T, a.cap)
    for s in shots:
        s["x_start"] = round(x_at(s["start"]), 1)
        s["x_end"] = round(x_at(s["end"]), 1)
        s["x_start_px"] = round(x_at(s["start"]) * vw / 100)
        s["x_end_px"] = round(x_at(s["end"]) * vw / 100)
        s["enters_frame"] = s["shot"] == 1
        s["exits_frame"] = s["shot"] == len(shots)

    per_second = [{"t": t, "x": round(x_at(t), 2), "x_px": round(x_at(t) * vw / 100),
                   "front_edge": round(x_at(t) + w_pct / 2, 2), "rear_edge": round(x_at(t) - w_pct / 2, 2)}
                  for t in range(0, int(math.floor(T)) + 1)]
    if per_second[-1]["t"] != T:
        per_second.append({"t": T, "x": round(x_at(T), 2), "x_px": round(x_at(T) * vw / 100),
                           "front_edge": round(x_at(T) + w_pct / 2, 2), "rear_edge": round(x_at(T) - w_pct / 2, 2)})
    if a.csv:
        with open(a.csv, "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=["t", "x", "x_px", "front_edge", "rear_edge"])
            wr.writeheader(); wr.writerows(per_second)

    arc = [("Entrance", 0, .10), ("Establish", .10, .25), ("Personality", .25, .70), ("Build-up", .70, .85), ("Exit", .85, 1.0)]
    arc = [{"phase": n, "from": round(T * s, 1), "to": round(T * e, 1),
            "x_from": round(x_at(T * s), 1), "x_to": round(x_at(T * e), 1)} for n, s, e in arc]

    gw, gh = (float(q) for q in a.gen_aspect.split(":"))
    strip_h = vw * gh / gw
    gen_pct = mascot_h / strip_h * 100
    lo, hi = WINDOW[a.aspect]
    warnings = []
    if not lo <= pct <= hi:
        warnings.append(f"Final mascot height {pct}% is outside the comfortable window {lo}-{hi}% for {a.aspect}.")
    if gen_pct < 10:
        warnings.append(f"Mascot is only {gen_pct:.0f}% of the generated frame: too small to generate cleanly. Use a taller generation aspect, a larger --mascot-pct, or the highest resolution the tool offers.")
    elif gen_pct < 15:
        warnings.append(f"Mascot is {gen_pct:.0f}% of the generated frame: small. Generate at the highest resolution and check face detail in the storyboard.")
    if gen_pct > 45:
        warnings.append(f"Mascot is {gen_pct:.0f}% of the generated frame: no room for flying or jumping. Use a taller generation aspect or a lower --mascot-pct.")
    feet = a.bottom_margin_pct / 100 * vh + (100 - a.ground_pct) / 100 * strip_h

    geo = {"video_px": [vw, vh], "strip_px": [vw, round(strip_h)], "gen_aspect": a.gen_aspect,
           "final_mascot_pct_of_video_height": pct, "final_mascot_px": round(mascot_h),
           "mascot_width_px_estimate": round(mascot_w), "mascot_width_pct_of_frame": round(w_pct, 2),
           "gen_mascot_pct_of_frame_height": round(gen_pct, 1), "ground_pct": a.ground_pct,
           "feet_height_above_video_bottom_px": round(feet)}
    motion = {"start_centre_x": round(x0, 2), "end_centre_x": round(x1, 2),
              "carry_speed_pct_per_s": round(v, 3), "carry_speed_px_per_s": round(v_px, 1),
              "carry_speed_mascot_heights_per_s": round(heights_per_s, 2),
              "fully_inside_frame_at_s": round(t_inside, 1), "front_edge_reaches_right_edge_at_s": round(t_exit_start, 1)}
    res = {"duration": T, "cap": a.cap, "motion": motion, "shots": shots, "arc": arc,
           "geometry": geo, "per_second": per_second, "warnings": warnings}
    if a.json:
        print(json.dumps(res, indent=2)); return

    print(f"Run time {T:g}s | cap {a.cap:g}s | {len(shots)} shot(s) | CONSTANT carry speed, no pauses\n")
    print(f"Carry speed: {v:.3f}% of frame width per second = {v_px:.1f} px/s = {heights_per_s:.2f} mascot-heights per second")
    print(f"  (a natural walk is about 1.0 mascot-height per second, so the ground carries the mascot much more slowly than it can walk: write walking as a treadmill-style walk)")
    print(f"  t=0: front edge at {a.sliver_pct}% (centre {x0:.1f}%) | fully inside the frame at {t_inside:.1f}s | front edge reaches the right edge at {t_exit_start:.1f}s | fully gone at {T:g}s (centre {x1:.1f}%)\n")
    print("| Shot | Time | Length | centre x start -> end | px start -> end | Note |\n|---|---|---|---|---|---|")
    for s in shots:
        note = "mascot ENTERS from off-frame (front edge visible at 0.0s)" if s["enters_frame"] else ""
        if s["exits_frame"]: note = (note + "; " if note else "") + "mascot EXITS: rear edge leaves the right edge on the last frame"
        print(f"| {s['shot']} | {s['start']:g}-{s['end']:g}s | {s['length']:g}s | {s['x_start']}% -> {s['x_end']}% | {s['x_start_px']} -> {s['x_end_px']} | {note} |")
    print("\nStory arc (time and centre x):")
    for r in arc: print(f"- {r['phase']}: {r['from']}s-{r['to']}s, x {r['x_from']}% -> {r['x_to']}%")
    print(f"\nPosition every {a.step:g}s (full per-second table via --csv or --json):\n| time | centre x | x px | front edge | rear edge |\n|---|---|---|---|---|")
    t = 0.0
    while t <= T + 1e-9:
        print(f"| {t:g}s | {x_at(t):.1f}% | {round(x_at(t)*vw/100)} | {x_at(t)+w_pct/2:.1f}% | {x_at(t)-w_pct/2:.1f}% |")
        t += a.step
    if abs((t - a.step) - T) > 1e-9:
        print(f"| {T:g}s | {x_at(T):.1f}% | {round(x_at(T)*vw/100)} | {x_at(T)+w_pct/2:.1f}% | {x_at(T)-w_pct/2:.1f}% |")
    print(f"\nSize: video {vw}x{vh} ({a.aspect}); strip {vw}x{geo['strip_px'][1]} generated in {a.gen_aspect}")
    print(f"Final mascot height {pct}% of video height = {geo['final_mascot_px']} px (width about {geo['mascot_width_px_estimate']} px = {geo['mascot_width_pct_of_frame']}% of frame width, at --mascot-aspect {a.mascot_aspect})")
    print(f"= {geo['gen_mascot_pct_of_frame_height']}% of the generated frame height; ground line at {a.ground_pct}% of generated frame height; feet about {geo['feet_height_above_video_bottom_px']} px above the video bottom")
    for w in warnings: print("WARNING:", w)


if __name__ == "__main__":
    main()
