# Size and placement (Phase 5) and storyboard (Phase 6)

Contents: size rules, running the planner, size preview prompt, storyboard prompts, verifying uploads, revising, checking the generated clips.

## Size and placement (Phase 5, gate 4)

The mascot layer is a full-width strip along the bottom of the video. The mascot must be readable but never dominate the video: not too big, not too small.

1. Confirm the frame the user already gave (9:16 or 16:9); ask only if it is missing.
2. Choose the final mascot height as a percentage of the video height:

| Frame | Comfortable window | Default | Why |
|---|---|---|---|
| 9:16 (1080x1920) | 5.5-8% (about 105-155 px) | 6.5% (125 px) | The travel axis is the narrow side, so the mascot must stay small; bigger covers captions and faces |
| 16:9 (1920x1080) | 10-14% (about 108-150 px) | 12% (130 px) | The frame is wide, so the same pixel size reads as a smaller share of the picture |

   Adjust inside the window for the design: very detailed or low-contrast mascots go to the top of the window; simple bold shapes can go lower. Objects with a small footprint (coin, pick) can be at the lower end; tall animals or wide objects keep their real proportions, so size by the body dimensions sheet (use the overall height, including the signature item, as the mascot height).
3. Run the planner to get the numbers and warnings:
```bash
python scripts/plan_shots.py --duration <s> --cap <cap> --aspect <9:16|16:9> --gen-aspect <21:9|16:9> --mascot-pct <chosen> --mascot-aspect <width/height of the mascot incl. cape or tail, from the dimensions sheet>
```
   It prints the strip size, the final mascot height and estimated width in pixels, the mascot height as a % of the generated frame (the number that goes into every shot prompt), and the constant carry speed that depends on the mascot's width. If it warns that the mascot is too small in the generated frame, follow the warning (higher resolution, taller generation aspect, a larger percentage inside the window).
4. Placement: the strip's bottom edge sits at the video's bottom edge by default; the feet end up a little above the bottom (the planner prints how many pixels). If the platform's captions or buttons cover the bottom of the video (reels, shorts), offer to raise the strip with `--bottom-margin-pct`.
5. Tell the user the final numbers in plain words ("about 125 px tall on a 1080x1920 video, 6.5% of the height").

### Size preview prompt (offer it, give it if the user wants to see)

Ask: "Do you want to see how big the mascot will look in your frame?" If yes, give an image prompt in the user's frame (9:16 for vertical, 16:9 for landscape). Attach the approved character sheet.

```
SIZE PREVIEW
A <9:16 vertical or 16:9 horizontal> video frame filled with a flat <locked colour name and HEX>. At the bottom of the frame, <X>% of the frame width from the left edge, stands the approved character from the attached sheet, full body, side view facing screen right, at exactly <final mascot height>% of the frame height, with its feet <feet-height>% of the frame height above the bottom edge. Nothing else is in the frame. <Style wording>. Neutral even lighting.
```

If the user wants a more realistic test, offer a sample frame: the same prompt but with "a plain mid-grey photo of <a person talking to camera / a product / a landscape> filling the frame behind the character". Then ask whether the size is right, and adjust the percentage if not. Re-run the planner after any change.

## Storyboard (Phase 6, gate 5)

Run the planner for the shot plan, create the handoff cards, and only then write storyboard prompts. The storyboard is the exact preview of each shot, so the user sees how it will look before spending generations.

Per shot, one storyboard image: 4 panels stacked vertically (start, one-third, two-thirds, end of the shot; use 5-6 panels for 30 s shots), each panel a full frame of the generated strip with the locked background colour. Because the mascot is carried at a constant speed, the centre x of the panels rises by equal steps (take the values from the planner's position table). The first panel of shot 1 shows only the front edge of the mascot inside the left edge; the last panel of the last shot shows the rear edge leaving the right edge. In every other joint, the last panel of shot N and the first panel of shot N+1 are the same picture.

```
STORYBOARD - SHOT <n> (<t0>-<t1> s)
Attached references: character sheet (identity), expression sheet (faces), action sheet (poses).
One tall image with <4> equal panels stacked top to bottom, separated by thin mid-grey gaps. Each panel is a full <21:9 or 16:9> video frame with a flat <colour and HEX> background. In every panel the same character is <gen%> of the panel height, the ground line is at <ground%> of the panel height, camera static and side-on. A small caption under each panel gives its time and centre x.
Panel 1 (t=<..> s, centre x=<..>%): <pose while carried, facing, expression label, state of the signature item>.
Panel 2 (t=<..> s, centre x=<..>%): <...>.
Panel 3 (t=<..> s, centre x=<..>%): <...>.
Panel 4 (t=<..> s, centre x=<..>%): <this is the Handoff Card for this shot, word for word>.
<Style wording>. Neutral even lighting.
```

Give all storyboard prompts at once (one per shot), or shot by shot if the user prefers. Tell the user to generate each, then upload them.

## Verifying the uploaded storyboards

Check every upload and report it as a short table: shot, what matches, what to fix.

1. Run the measuring script on each upload (it splits the panels and measures the mascot):
```bash
python scripts/check_frame.py <storyboard.png> --bg <green|black|white> --grid 1x<panels> --expect-height <gen%> --expect-x <x1,x2,x3,x4>
```
   Interpret its flags: background not flat or the wrong colour; mascot height more than 25% off (crouches and flights legitimately differ); x more than 4% off the plan. Positions at the entrance and exit are measured on the visible part of the mascot only.
2. Look at the images and compare against the approved sheets: identity (face, hair or markings, outfit, signature item and its exact colour), style, expression label, the planned pose and facing.
3. Continuity: compare the last panel of shot N with the first panel of shot N+1 for the same x, height, pose and walk-cycle phase, facing, expression and signature-item state.
4. Constant speed: the x-positions of the panels step forward evenly with time; nothing sits still or jumps ahead.
5. Story: does each shot show the planned beats, with the mascot entering only in shot 1 and leaving only in the last shot?

Then say "approved" or give specific fixes. A fix is one of: a changed storyboard prompt (identity, colour, background wording), a changed action or timing (go back to the Action Plan), or a changed handoff pose. Re-check after the user regenerates. Whenever the user changes an action, update the action plan, the affected sheets (action and workflow) if the pose is new, the handoff cards and the storyboard, and re-post the Project Brief.

Gate 5 passes only when the user says the storyboard matches what they want. The next step is the final prompts, which are delivered all at once.

## Checking the generated clips (after Phase 7, when the user returns with videos)

Offer this when the user has generated the clips. For each clip, and for each joint:

```bash
python scripts/track_motion.py shot1.mp4 --bg <green|black|white> --expect-speed <carry speed %/s from the planner> --role first
python scripts/track_motion.py shot2.mp4 --bg <...> --expect-speed <...> --role middle
python scripts/track_motion.py shot6.mp4 --bg <...> --expect-speed <...> --role last
python scripts/track_motion.py --joint shot1.mp4 shot2.mp4 --bg <...>
```

The speed check reports the fitted speed, wobble around a straight line and stalls; the joint check compares the last frame of shot N with the first frame of shot N+1 (x, size, feet height, pixel difference). Report flags in plain words and give the fix: regenerate the shot with the previous Handoff Card pasted word for word and the previous last frame as the start image, restate the MOTION LOCK, or trim the first frames at the joint in the edit.
