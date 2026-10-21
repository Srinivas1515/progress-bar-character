# Editing guide (delivered with the final prompts)

Contents: before you start, assemble the track, place it, remove the background, position and speed check, export, troubleshooting.

Use generic menu names (clip, scale, position, blend mode, key, keyframe); the same functions exist in CapCut, Premiere, DaVinci Resolve, After Effects, VN and similar editors. If the user names their editor, use its terms. Tailor the answer: keep only the row for the locked background colour, the user's numbers from the planner, and the troubleshooting rows that fit.

## Before you start

You need the main video, the mascot shots in order, and the planner's checkpoint table (time, % and px). Mute the mascot track: the clips are silent, and stray audio would collide with the soundtrack.

## 1. Assemble the mascot track

1. Put the shots one after another, end to end, on ONE mascot track in shot order. Never stack the shots as separate layers. Use hard cuts, not dissolves: the handoff frames match, so each joint should be invisible.
2. If a generator adds slightly different first frames, trim up to 6 frames at the joint, and trim the same amount from the end of the previous shot only if the carry speed stays even.
3. The total length of the mascot track must equal the main video's length. If it differs by a second or two, change the speed of ALL mascot clips by the same percentage (at most 5%) so the carry speed stays constant and the mascot still leaves the frame on the last frame. Do not stretch or shorten one clip on its own.
4. Check that the mascot enters at 0.0 s (front edge already at the left edge) and its rear edge leaves the right edge on the last frame of the main video.

## 2. Place it

1. Put the mascot track above the main video.
2. Scale the clip so its width equals the video width (the planner prints the strip size).
3. Put the clip's bottom edge on the video's bottom edge, or raise it by the margin you chose for platform captions and buttons.
4. For a 16:9 clip generated for a 21:9 strip, crop it top and bottom to the strip, keeping the ground line inside the crop.

## 3. Remove the background

| Locked colour | Method | Settings |
|---|---|---|
| Green `#00FF00` | Chroma key | Pick the green; tolerance up until the background disappears; edge feather 1-2 px; spill suppression on to remove green on edges |
| Black `#000000` | Screen (or Add / Lighten) blend | Layer opacity 100%; if the editor has no blend modes, use a luma key on black |
| White `#FFFFFF` | Multiply (or Darken) blend | Layer opacity 100%; if no blend modes, use a luma key on white |

Notes:
- Under Screen, dark pixels in the mascot (black hair, dark clothes) become see-through. If it shows, lift the mascot's blacks by 5-10% (levels) or switch to green.
- Under Multiply, light pixels in the mascot take the colour of the video behind them. If a bright halo shows, pull the white point down 3-5% before blending or switch to green.
- With chroma key, thin hair, glass and motion blur key badly; fix with edge feather or choose black or white next time.
- The signature colour survives all three methods. If it shifts, check that no colour effect is applied to the layer.

## 4. Position and speed check

Scrub to the times in the planner's position table. The mascot's centre should be within 3% of the frame width of the listed x. Because the carry speed is constant, the position must rise steadily: it never pauses and never jumps.
- If you have the generated clips, run `scripts/track_motion.py` on each clip (speed, stalls, wobble) and on each joint (position, size, feet height, pixel difference). See `size-and-storyboard.md`.
- If a clip is carried too slowly or too fast, regenerate it with the MOTION LOCK restated, or apply the small same-percentage speed change to all clips (step 1.3), not to one clip.
- If a joint jumps, regenerate the later shot with the previous Handoff Card word for word and the last frame as a start image.

## 5. Export

Export at the main video's resolution and frame rate. Watch the file once at full length with sound: the mascot enters at the start, moves steadily without stopping, nothing jumps at a joint, and it leaves on the last frame.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Face or outfit differs between shots | Identity drift | Regenerate the later shot with the previous shot's last frame as the start image, the sheets as references, and the short identity lock in POSITIVE LOCKS |
| Signature colour shifts | Lighting or grade differences | Restate the colour with hex and "same in every frame"; remove any colour grade |
| Background not flat | Generator added a floor, shadow, vignette or noise | Levels or key in the edit; repeat the background block in POSITIVE LOCKS; check with `scripts/check_frame.py` on a frame |
| Mascot jumps at a joint | Different pose or x at the handoff | Trim the first frames of the new shot; regenerate with the previous Handoff Card pasted word for word |
| Mascot looks stuck or surges | The generator ignored the carry speed | Regenerate with the MOTION LOCK restated and the speed in px per second; check with `track_motion.py` |
| Mascot reaches the right edge early or late | Carry speed off, or total length mismatch | Apply the same small speed change (up to 5%) to all clips, or regenerate the clip that drifted |
| Mascot too big or small on the video | Size set at generation | Rerun the planner with another `--mascot-pct` and regenerate, or crop the strip |
| Green edges after keying | Green spill | Spill suppression, edge feather, or regenerate with "neutral white ambient light" |

To measure a generated clip, grab a frame (`ffmpeg -ss <time> -i clip.mp4 -frames:v 1 frame.png`) and run `scripts/check_frame.py` on it.
