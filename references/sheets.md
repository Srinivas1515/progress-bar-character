# Sheets (Phases 2 and 4)

Contents: what Claude can and cannot do, the shared sheet look, the character sheet, the four support sheets, object variant, animal variant, logo variant, existing-mascot variant, reviewing an uploaded sheet.

## What Claude does here

Claude cannot render images in this chat. For each sheet Claude writes a ready-to-paste prompt for the user's image generator, the user generates it and uploads the result, and Claude reviews the upload against the brief (identity, style, layout, background, lighting, labels) and either approves it or lists exact fixes with an improved prompt. State this once, at the first sheet.

For identity consistency, tell the user to attach the approved character sheet as a reference when generating every later sheet, and to use the same image tool and settings for all of them.

## The shared sheet look (applies to every sheet)

Every reference sheet uses a flat, neutral mid-grey background and ordinary general lighting, not studio lighting. Put this block into every sheet prompt, unchanged:

```
SHEET LOOK
Background: flat neutral mid-grey (about #808080), uniform from edge to edge, with no gradient and no vignette.
Lighting: ordinary even ambient light, like soft daylight in a normal room, coming from above and slightly in front; shadows are soft, low-contrast and short. The sheet has no rim light, no dramatic key light, no spotlight, no coloured light and no glossy studio highlights.
Layout: clean, evenly spaced, nothing overlapping, each view at the same scale, plain capital-letter labels under each view.
Style: <the exact animation style wording from the Project Brief>
```

Do not use the locked background colour (green, black or white) on sheets. That colour is only for shots, storyboards and the size preview.

## Character sheet (Phase 2, gate 1)

```
CHARACTER SHEET
A character design sheet of <one-line character: age, person type, build, personality>, designed for a progress-bar mascot in a video about <video topic>.
Views, all full-body at the same scale and height: FRONT VIEW, BACK VIEW, LEFT PROFILE, RIGHT PROFILE, THREE-QUARTER FRONT VIEW, THREE-QUARTER BACK VIEW.
Detail panels: CLOSE-UP of the face, SIGNATURE ITEM detail (<cape / scarf / hat / bag / ...>) with its texture, FOOTWEAR detail, HANDS detail.
Outfit: <each garment, colour, material>. Signature item: <item, colour with hex, shape>. Hair: <description and silhouette>.
Palette strip: 5-8 colour swatches with HEX codes for skin, hair, outfit pieces and the signature item.
<SHEET LOOK block>
```

Before writing it, make sure it fits the Project Brief: design the mascot from the video (brand uniform and colours for an ad; costume that fits the genre for a song; DJ gear for a DJ track). Run the background-colour clash check from `discovery.md` against the palette and tell the user if it fails.

At gate 1 the user either approves or asks for changes. Revise the sheet prompt until approved. Nothing after this is created before approval.

## Support sheets (Phase 4, gate 3)

Created only after the character sheet is approved AND the action plan is locked, so the sheets contain exactly the poses and faces the plan needs. Each is its own sheet and its own image. Attach the approved character sheet to each prompt. Use the SHEET LOOK block on all four.

### 1. Expression sheet

```
EXPRESSION SHEET
Head-and-shoulders portraits of the same character in <12> labelled expressions: <HAPPY, SAD, ANGRY, SURPRISED, SCARED, DISGUSTED, CONFUSED, DETERMINED, MISCHIEVOUS, PROUD, EXCITED, TIRED, plus any the action plan needs, e.g. SINGING, SMUG>. Two rows, equal size, one label under each. Eyebrows, eyes, mouth and head tilt are clearly different in every portrait; hair, outfit and the signature item are identical in all.
<SHEET LOOK block>
```

Adapt the labels to the personality and the plan: a song mascot may need SINGING and VIBING, an ad mascot SMUG and WELCOMING. Keep 9-12 faces.

### 2. Action sheet

```
ACTION SHEET
The same character in <12-16> labelled full-body poses, at the same scale, drawn from the side (the direction of travel is screen right) unless a pose reads better from the front: <list every pose the action plan uses, e.g. ENTRANCE LANDING, STANDING IDLE, HERO POSE (BACK VIEW), TURN, WAVE, WALK CONTACT, WALK PASSING, CROUCH, TAKE-OFF, FLYING, EXIT POSE>. Each pose shows the signature item in its correct state for that pose. Every pose is something the mascot can do while being carried to the right on a moving ground, with its feet planted.
<SHEET LOOK block>
```

### 3. Action workflow sheet

The workflow sheet shows how each action unfolds over time: anticipation, the action itself, follow-through and settle.

```
ACTION WORKFLOW SHEET
For each action, one horizontal strip of <5-8> numbered key drawings of the same character, side view, left to right, with small arrows showing the direction of motion and the path of the signature item: <ACTION 1 e.g. ENTRANCE>, <ACTION 2 e.g. WALK CYCLE (contact, down, passing, up)>, <ACTION 3 e.g. CROUCH TO TAKE-OFF>, <EXIT>. Under each drawing: its number and its time in seconds (for example 0.0 s, 0.4 s, 0.8 s). Walk cycles are drawn treadmill-style: feet planted, legs at a natural rhythm. A final strip, HANDOFF POSE, shows the exact steady pose, including the walk-cycle phase, in which a clip ends and the next clip begins.
<SHEET LOOK block>
```

### 4. Body dimensions sheet

```
BODY DIMENSIONS SHEET
Front, side and back views of the same character, flat and straight on, at the same scale, with thin dimension lines and labels: TOTAL HEIGHT = <N> HEADS, HEAD WIDTH, SHOULDER WIDTH, ARM LENGTH, LEG LENGTH, FOOT LENGTH, <SIGNATURE ITEM> LENGTH as a percentage of total height, plus a SILHOUETTE row and a SIZE COMPARISON strip (character next to a simple unit block of 1 head). Use ratios, not real-world units.
<SHEET LOOK block>
```

Use the dimensions sheet later for the size rule in `size-and-storyboard.md`.

Present the four sheets one at a time, or all four prompts together if the user prefers. Approve each upload before treating gate 3 as passed.

## Object variant

For an object mascot (ball, paper plane, guitar pick, scooter, product) the sheets change as follows.
- **Object design sheet** instead of a character sheet: FRONT, BACK, SIDE, TOP and THREE-QUARTER views, a material and colour callout with HEX codes, and callouts naming each part.
- **Mechanics sheet** replaces the movement part of the expression sheet: how the object moves, as a real object would. Show the axes and joints (what rolls, rotates, hinges, bends, springs), the way it travels (rolls, hops, glides, hovers, rides), its limits (it cannot walk if it has no legs), and squash-and-stretch rules (a ball squashes on contact; a paper plane banks into turns; a coin spins on its edge).
- **State sheet** replaces the expression sheet: 8-10 labelled states shown with small changes that do not need a face (HAPPY: bouncier, brighter light; TIRED: slower, drooping; SURPRISED: sudden jump). If the object has a face, use the standard expression labels.
- Action sheet, action workflow sheet and body dimensions sheet work as above, using the object's own movement.

## Animal variant

For an animal mascot be faithful to the species.
- **Animal sheet** instead of a character sheet: real anatomy and proportions of the species, stylised only by the chosen style. Views: FRONT, BACK, LEFT, RIGHT, THREE-QUARTER, plus detail panels (head, paws or feet, tail, ears, markings).
- **Expression sheet, in depth**: 12 or more expressions that use the features of the animal: eyes, ears (forward, back, flat), brows if present, mouth or beak or muzzle, whiskers, tail position, fur or feather puff, posture. Add a small BODY-LANGUAGE row showing neutral, happy, scared, alert, sleepy postures.
- **Action sheet**: the animal's natural gaits and behaviours: WALK, TROT, RUN or GALLOP, HOP or FLY or SWIM where relevant, sniff, scratch, shake, stretch, pounce, sit. Only actions the species can plausibly do.
- Workflow and dimensions sheets as above; dimensions include BODY LENGTH, LEG, TAIL and HEAD ratios.

## Logo variant (brand mascots)

When the mascot is a brand logo, treat it as an object with exact geometry.
- Get the logo as an image or vector. Describe its shapes, HEX colours and proportions in the sheet.
- The design sheet shows the logo flat, from the front, and in the "mechanical" forms the animation will use (for example, its parts separating and assembling, rolling, spinning, bouncing).
- Keep any text out of the animated mascot if possible: video generators distort letters. Animate the symbol and add the real wordmark in the edit instead, if the brand needs it. Say this to the user.
- The logo must stay recognisable and exactly in the brand colours in every frame.
- Only work on a logo the user says belongs to them or their client.

## Existing-mascot variant

If the user already has a character, object or animal:
1. Ask for the best image(s) or a clear description. Accept an existing sheet as it is if it is clear and usable; do not redo work that is done.
2. If the upload is a single picture, write the character-sheet prompt so that the generator matches the uploaded image 100% ("the uploaded reference is the only source for design, outfit and style") and keeps written description minimal. Style and palette come from the upload; the Project Brief style is then set to match it.
3. Build every other sheet from the approved version of that mascot. If their existing sheets use other backgrounds (white, dark), they are accepted for review; offer to regenerate them on mid-grey only if the user wants consistent sheets.

## Reviewing an uploaded sheet

Look at the image and check, in this order: identity matches the brief and earlier sheets (face, hair or markings, outfit, signature item and its colour); style is exactly the chosen one; every requested view or label is present and correct; mid-grey flat background; ordinary even lighting; same scale across views; no stray text or artefacts. Report in 3-6 lines: what is right, what to fix, then either "approved" or the revised prompt. Ask for the user's approval explicitly before moving on, and update the Project Brief status.
